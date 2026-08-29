# Related Work — annotated bibliography

> Convention: **BORROW** = wheel we reuse; **ADD** = delta we claim beyond it.
> `[verify]` = citation needs final check before submission. Classics are safe;
> arXiv IDs marked from search results 2026-08-24 unless noted.

## A. Temporal awareness of LLMs (nearest neighbors)

1. Cheng et al., *Your LLM Agents are Temporally Blind*, ACL Findings 2026,
   arXiv:2510.23853.
   BORROW: empirical proof agents assume stationary context even WITH
   timestamps (<65% human alignment); TicToc dataset; prompting fails,
   post-training partially fixes.
   ADD: they *align agents to human* time as a tool-use skill. We argue the
   deeper fix is a native time representation — alignment becomes translation
   between coordinate systems (§7).

2. *Discrete Minds in a Continuous World: Do Language Models Know Time
   Passes?*, arXiv:2506.05790.
   BORROW: token-time vs wall-clock-time as two measurement domains; evidence
   models use token-length as duration proxy and adapt under time pressure.
   ADD: their token-time is still chronometry. Our τ is experiential density;
   and continuity/discontinuity (C8) is absent there entirely.

3. Fatemi et al., *Test of Time*, ICLR 2025, arXiv:2406.09170 (+ benchmark
   family: TRAM 2024; TimeBench, Chu et al. 2024; TempReason, Tan et al. 2023;
   TIME, NeurIPS 2025).
   BORROW: the semantic/arithmetic decomposition; documented failure modes.
   ADD: all test time-as-content to reason ABOUT. None test time-as-experience
   structuring memory. That contrast is our §2.5 gap claim. `[verify exact
   cites for family]`

## B. Agent memory systems

4. Packer et al., *MemGPT*, arXiv:2310.08560.
   BORROW: OS-paging analogy, self-directed archival.
   ADD (from our survey): no consolidation, no decay policy, salience =
   mid-task attention; hoarding tendency.

5. Zhong et al., *MemoryBank*, AAAI 2024, arXiv:2305.10250.
   BORROW: R = e^(−t/S) — adopted as THE wall-clock baseline our E1 must beat.
   CRITIQUE-AS-CONTRIBUTION: t is wall-clock — a cargo-cult parameter. The
   curve's form derives from biological consolidation dynamics the agent lacks.

6. Park et al., *Generative Agents*, arXiv:2304.03442.
   BORROW: recency × importance × relevance retrieval triad.
   ADD: importance is a scored attribute, not an encoding-time durability
   tier; no anchors, no constellations, no reconstruction grading.

7. Gutiérrez et al., *HippoRAG*, arXiv:2405.14831. `[verify]`
   BORROW: hippocampal indexing theory via personalized-PageRank concept
   graphs. ADD: retrieval-only — borrows the index, skips the lifecycle
   (encoding gates, consolidation, forgetting).

8. *FOREVER*, arXiv:2601.03938.
   BORROW: **model-time ≠ wall-clock** — replay scheduled by accumulated
   optimizer-update magnitude. Closest philosophical ally; cite prominently.
   ADD: they schedule continual-learning replay; we extend native-time to
   agent episodic memory and define τ from experience density (novelty,
   prediction-error) rather than gradients — available to frozen models.

9. *Engram* (open-source cognitive substrate; GitHub tonitangpotato/engram-ai)
   `[verify publication status]`.
   BORROW: ACT-R activation, Ebbinghaus decay, Hebbian links, interoceptive
   hub — proof the substrate stack composes.
   ADD: its drives are hardcoded constants; ours are derived from the
   disanalogy catalog (what necessity substitutes for metabolism?).

10. *Human-Like Remembering and Forgetting in LLM Agents: An ACT-R approach*
    (ACM). `[verify full cite]`
    BORROW: base-level activation decay + probabilistic noise in agent memory.

## C. Cognitive-science foundations (the wheels)

11. James, *Principles of Psychology* (1890) — stream of consciousness → §7
    continuity. 12. Ebbinghaus (1885/1964) — decay curve origin. 13. Bartlett,
    *Remembering* (1932) — reconstructive recall; schema-consistent intrusions
    → H5's predicted error signature. 14. Atkinson & Shiffrin (1968); Tulving
    (1972; *Elements* 1983) — store taxonomy, episodic/semantic split. 15.
    Collins & Loftus (1975) — spreading activation → H10. 16. Gibbon (1977)
    Scalar Expectancy Theory; scalar variability → fuzzy-interval widths (H9).
17. McClelland, McNaughton & O'Reilly (1995), Complementary Learning Systems —
    fast/slow learners, interleaved-learning problem → curator/consolidator
    design and the frozen-model variant thereof. 18. Conway &
    Pleydell-Pearce (2000), Self-Memory System — lifetime periods ⊃ general
    events ⊃ specific knowledge → H7 + anchor hierarchy. 19. Zacks & Swallow
    — event segmentation at prediction-error boundaries → H4 fusion triggers +
    retrospective-duration effects. 20. Schacter, *Seven Sins of Memory* —
    adaptive forgetting frame. 21. Bergson, *Durée et simultanéité* lineage
    (1889–) — lived vs spatialized time; our chronometry/chronoception split.
22. Locke — psychological continuity → §7 identity discussion. 23.
    Droit-Volet & Meck — emotion-modulated timing `[verify]` → mood-distortion
    grounding. 24. Wittmann — felt passage of time `[verify]`.

## D. Motivation & drive substrates

25. Schmidhuber (1991; IEEE TAMD 2010) — compression-progress theory:
    curiosity/boredom formalized; subjective speed ∝ learning progress → τ
    definition + D8 (boredom as scheduling signal).
26. Lidayan et al., arXiv:2503.23631 — children vs AI agents, entropy/gain/
    empowerment objectives. 27. MOP, Nat. Commun. 2024 (s41467-024-49711-1)
    — behavior from occupying action-state path space; survival without
    reward-maximization. 28. Oudeyer & Kaplan; Barto — intrinsic-motivation
    surveys `[verify]`.

## E. Difference literature

29. Niu et al., arXiv:2409.02387 — comprehensive LLM/cog-sci review.
30. Nature Human Behaviour, "LLMs differ … because they are not embodied"
    (s41562-023-01723-5) `[verify authors]`. 31. Mahowald et al.,
    arXiv:2301.06627; Suresh et al., EMNLP 2023 — functional-competence gap;
    conceptual structure coherence difference.

## F. Secondary / color

32. CACM (Feb 2026), *How LLMs Make Sense of Time*. 33. Zylos research note
    (Apr 2026) — practitioner synthesis; four sub-problems decomposition.
