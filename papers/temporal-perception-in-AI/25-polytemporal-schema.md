# Polytemporal Schema v1 — normalized, typed coordinates

> Design rule (hard-won): coordinates are the QUERY surface. They get real
> types and indexes — no JSONB on any path a mechanism reads. Extensibility
> comes from ALTER TABLE + lookup tables, not from string parsing.
> Sparse numeric EAV exists solely as an experiment sandbox, off hot paths.

## Lookup tables (small, cached, self-documenting)

```sql
CREATE TABLE lu_kind      (id smallint PRIMARY KEY, name text);  -- snapshot|message|thread_summary|...
CREATE TABLE lu_tier      (id smallint PRIMARY KEY, name text);  -- normal|flashbulb|protected
CREATE TABLE lu_provenance(id smallint PRIMARY KEY, name text);  -- witnessed|boundary|reconstructed
CREATE TABLE lu_precision (id smallint PRIMARY KEY, name text);  -- exact|phase_of_day|relative_anchor|inferred
CREATE TABLE lu_dayclass  (id smallint PRIMARY KEY, name text);  -- workday|weekend|holiday|event_window
CREATE TABLE regime_cycle (id smallint PRIMARY KEY, name text);  -- named cycles: 'clash-weekend','fiscal-year',...
CREATE TABLE person       (pid text PRIMARY KEY, key_ref text);  -- pseudonymous; name-key external
```

## Episodes

```sql
CREATE TABLE episode (
  id            uuid PRIMARY KEY,
  persons       text[] NOT NULL,

  kind          smallint NOT NULL REFERENCES lu_kind(id),

  -- ── polytemporal vector (typed, indexed) ──────────────
  wall          timestamptz,          -- human interface; payload attribute
  mono          bigint,               -- capture-stream ordering
  tau           double precision NOT NULL,  -- subjective time ∫ novelty-density
  fuzz          tstzrange,            -- [t_lo,t_hi]; width = encoding confidence
  cycle_id      smallint REFERENCES regime_cycle(id),
  phase_idx     smallint,             -- position within cycle
  day_class     smallint REFERENCES lu_dayclass(id),
  precision_src smallint REFERENCES lu_precision(id),
  -- ────────────────────────────────────────────────────────

  salience      real CHECK (salience BETWEEN 0 AND 1),
  tier          smallint NOT NULL DEFAULT 1 REFERENCES lu_tier(id),
  strength      double precision,     -- decay S; flashbulb => 'Infinity'
  provenance    smallint REFERENCES lu_provenance(id),

  subject_norm  text,
  body_embed    vector(768)
);

CREATE INDEX episode_tau_idx    ON episode (tau);
CREATE INDEX episode_fuzz_idx   ON episode USING gist (fuzz);
CREATE INDEX episode_regime_idx ON episode (cycle_id, phase_idx);
CREATE INDEX episode_embed_idx  ON episode USING hnsw (body_embed vector_cosine_ops);
CREATE INDEX episode_person_idx ON episode USING gin (persons);
```

## Constellation graph

```sql
CREATE TABLE anchor_edge (
  episode_id uuid REFERENCES episode ON DELETE CASCADE,
  anchor_id  uuid REFERENCES episode,
  rel        smallint REFERENCES lu_rel(id),   -- before|during|after|within
  qualifier  text,                             -- 'week','day','noon-to-sunset'
  PRIMARY KEY (episode_id, anchor_id)
);
CREATE TABLE lu_rel (id smallint PRIMARY KEY, name text);
CREATE INDEX anchor_edge_anchor_idx ON anchor_edge (anchor_id);
```

## Thread structure (mail pilot)

```sql
CREATE TABLE thread (
  id uuid PRIMARY KEY,
  root_episode uuid REFERENCES episode,
  period_id uuid                       -- optional container ref
);
CREATE TABLE message_edge (
  msg_episode uuid REFERENCES episode,
  thread_id uuid REFERENCES thread,
  in_reply_to uuid REFERENCES episode, -- References:/In-Reply-To chain
  latency_ms bigint                     -- response task-time
);
```

## Experimental sandbox (NOT for mechanisms)

```sql
CREATE TABLE episode_coord (
  episode_id uuid REFERENCES episode ON DELETE CASCADE,
  coord_id   smallint,                  -- registered per-hypothesis
  val        double precision,
  PRIMARY KEY (episode_id, coord_id)
);
-- graduated coords promote: ALTER TABLE episode ADD COLUMN ... (+ backfill)
```

## Canonical mechanism queries (projections)

```sql
-- Decay-ranked recall (E1 core):
SELECT id FROM episode
 WHERE tier <> 3   -- non-flashbulb first
 ORDER BY strength * exp(-( $tau_now - tau) / NULLIF(strength,'Infinity'::float8)) DESC NULLS FIRST
 LIMIT k;

-- Interval probe ("between noon and sunset"):
SELECT * FROM episode WHERE fuzz && $window;

-- Constellation walk ("what happened around the sale?"):
WITH RECURSIVE spread AS (
  SELECT episode_id FROM anchor_edge WHERE anchor_id = $a
  UNION
  SELECT ae.episode_id FROM anchor_edge ae JOIN spread s USING (anchor_id)
) SELECT * FROM spread;
```

## Open problems (research, not engineering)

1. τ calibration — units; cross-body τ unification (mail stream vs bot stream).
2. Salience function — feature weights unknown until E-series runs.
3. Anchor detection threshold — hub-vs-satellite criterion; the pilot domain's ownership-transfer event is our labeled example.
