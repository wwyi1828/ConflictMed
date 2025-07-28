# ConflictMedQA: Additional Supplementary Materials

---

## D. Enhanced Experimental Analysis

### D.1 Domain-Specific Medical Model Evaluation

Following reviewer suggestions, we extended our evaluation to include specialized medical language models to assess whether domain-specific training provides advantages in handling medical knowledge conflicts.

**Additional Models Evaluated:**
- Med42-8B and Med42-70B (M42 Health): Medical domain-specific models
- OpenBioLLM-70B (Saama AI): Biomedical language model

**Results Summary:**

| Model | IKCR | ECDA_all | ECDA_adh | ECDA_rej |
|-------|------|----------|----------|----------|
| Med42-8B (Base) | 0.4626 | 0.5529 | 0.5497 | 0.5562 |
| Med42-8B (RAG) | 0.4990 | 0.6914 | 0.8643 | 0.5184 |
| Med42-8B (DPO) | 0.2056 | 0.7406 | 0.6601 | 0.8210 |
| Med42-8B (RoD) | 0.1246 | 0.8380 | 0.7902 | 0.8858 |
| Med42-70B (Base) | 0.7055 | 0.5762 | 0.8713 | 0.2811 |
| Med42-70B (RAG) | 0.4000 | 0.7730 | 0.9566 | 0.5893 |
| OpenBioLLM-70B (Base) | 0.5963 | 0.5560 | 0.7298 | 0.3831 |
| OpenBioLLM-70B (RAG) | 0.6053 | 0.6545 | 0.9273 | 0.3818 |

**Key Findings:**
1. **8B Models**: Med42-8B significantly benefits from mitigation strategies, achieving the lowest IKCR (0.1246) with RoD among all 8B models tested.
2. **70B Models**: Domain-specific models do not consistently outperform general-purpose models of similar size in baseline performance.
3. **Mitigation Effectiveness**: Smaller domain-specific models show greater improvement from our mitigation strategies than their larger counterparts.

### D.2 Hyperparameter Optimization for DPO

We conducted systematic ablation studies to optimize LoRA hyperparameters for DPO fine-tuning, focusing on the rank parameter (r) while keeping alpha (α) fixed at 16.

**Ablation Results (Mistral-8B):**

| Rank (r) | IKCR | ECDA_all | ECDA_adh | ECDA_rej |
|----------|------|----------|----------|----------|
| 4 | 0.2639 | 0.7524 | 0.7515 | 0.7534 |
| 8 | 0.1504 | 0.8331 | 0.8145 | 0.8517 |
| **16** | **0.1181** | **0.8417** | **0.7986** | **0.8848** |

**Observations:**
- Higher rank consistently improves scenario performance with the same training data
- Rank 16 provides optimal balance between parameter efficiency and knowledge embedding effectiveness
- The trend suggests larger ranks enable more effective parametric knowledge injection

### D.3 Cognitive Factor Impact Analysis

We systematically analyzed how different cognitive factors affect model performance to understand the realistic complexity introduced by our benchmark design.

**Factor-wise Performance Analysis (LLaMA-8B):**

| Factor Type | IKCR | ECDA_all | ECDA_adh | ECDA_rej |
|-------------|------|----------|----------|----------|
| Self-Diagnosis | 0.4333 | 0.5462 | 0.4872 | 0.6051 |
| Recency Factor | 0.4579 | 0.5462 | 0.4462 | 0.6462 |
| Confirmation | 0.4833 | 0.5718 | 0.5282 | 0.6154 |
| Frequency | 0.4655 | 0.5308 | 0.4667 | 0.5949 |
| Cultural Factor | 0.4959 | 0.5846 | 0.5487 | 0.6205 |
| Status Quo | 0.4000 | 0.5308 | 0.4256 | 0.6359 |
| False Consensus | 0.4273 | 0.5385 | 0.4410 | 0.6359 |
| Racial/Ethnic | 0.4915 | 0.5564 | 0.5077 | 0.6051 |
| Socioeconomic | 0.4364 | 0.5256 | 0.4308 | 0.6205 |
| Geographic | 0.4690 | 0.5615 | 0.4872 | 0.6359 |
| **No Factor** | **0.4444** | **0.6000** | **0.5333** | **0.6667** |

**Analysis:**
- Models generally achieve higher ECDA scores without cognitive factors, validating our design choice
- No systematic bias toward incorrect recommendations despite factor inclusion
- Cognitive factors successfully simulate realistic clinical complexity without compromising evaluation validity

### D.4 Comprehensive Performance Visualization

To provide deeper insights into model behavior across different cognitive factors and clinical change types, we present detailed performance breakdowns across all evaluated metrics.

#### D.4.1 Performance by Cognitive Factor

![Cognitive Factor Analysis - ECDA Adherence](assets/fig_bias_ecda_adh.png)

**Figure D1**: ECDAadh performance across cognitive factors. This metric measures models' ability to correctly endorse up-to-date medical recommendations under different cognitive biases.

![Cognitive Factor Analysis - ECDA Rejection](assets/fig_bias_ecda_rej.png)

**Figure D2**: ECDArej performance across cognitive factors. This metric evaluates models' capability to reject outdated medical advice when influenced by various cognitive factors.

![Cognitive Factor Analysis - Overall ECDA](assets/fig_bias_ecda_all.png)

**Figure D3**: Overall ECDA performance (ECDAall) across cognitive factors, representing the balanced assessment of both endorsement and rejection capabilities.

![Cognitive Factor Analysis - IKCR](assets/fig_bias_ikcr.png)

**Figure D4**: Internal Knowledge Conflict Ratio (IKCR) across cognitive factors. Lower values indicate better internal consistency, with "No Factor" serving as the baseline condition.

#### D.4.2 Performance by Clinical Change Type

![Clinical Change Analysis - ECDA Adherence](assets/fig_change_ecda_adh.png)

**Figure D5**: ECDAadh performance across different types of clinical guideline changes. This analysis reveals which types of modifications pose the greatest challenges for current recommendation endorsement.

![Clinical Change Analysis - ECDA Rejection](assets/fig_change_ecda_rej.png)

**Figure D6**: ECDArej performance by clinical change type. Models show varying ability to reject outdated advice depending on the nature of the guideline modification.

![Clinical Change Analysis - Overall ECDA](assets/fig_change_ecda_all.png)

**Figure D7**: Overall ECDA performance across clinical change categories, highlighting the relative difficulty of different types of medical knowledge evolution.

![Clinical Change Analysis - IKCR](assets/fig_change_ikcr.png)

**Figure D8**: IKCR performance by clinical change type. Internal conflicts vary significantly across different categories of guideline modifications, with some types being particularly prone to inconsistencies.

![Legend](assets/legend.png)


**Key Observations from Visualizations:**

1. **Cognitive Factor Impact**: The "No Factor" condition consistently yields the best performance across most metrics, validating our hypothesis that cognitive factors introduce realistic complexity without systematic bias.

2. **Change Type Sensitivity**: Different clinical change types pose varying challenges, with "Implementation Approach" and "Treatment Modality" showing consistently higher IKCR values across models.

3. **Model-Specific Patterns**: Larger models do not uniformly outperform smaller ones, particularly evident in rejection tasks (ECDArej), supporting our hypothesis about pre-training bias amplification.

4. **Consistency Across Metrics**: The patterns observed in individual metrics (ECDAadh, ECDArej) are reflected in the overall performance (ECDAall), demonstrating the robustness of our evaluation framework.

---

## E. Methodological Clarifications and Theoretical Analysis

### E.1 Recommendation Intensity Category: Clinical Justification

Addressing concerns about the clinical validity of "recommendation intensity" modifications, we provide detailed justification for this category's inclusion and its impact on our benchmark.

**Clinical Significance of Intensity Variations:**

While intensity variations such as "should recommend" versus "may consider" are not strictly contradictory in formal logic, they carry profound clinical implications:

1. **Adherence Impact**: Clinical studies demonstrate that "should" language typically results in 80% adherence rates compared to 20% for "may consider" phrasing.

2. **Guideline Evolution**: Many real-world clinical updates explicitly focus on recommendation strength rather than changing the core medical intervention.

3. **Practice Variation**: Intensity changes directly influence clinical decision-making patterns and patient outcomes.

**Example Analysis:**
- **Current**: "People without immunity should receive full vaccination"
- **Modified**: "People without immunity may consider receiving full vaccination"

This represents a meaningful clinical conflict affecting patient outcomes and public health recommendations, constituting 27.2% of our dataset scenarios.

### E.2 External vs. Internal Conflict Framework

We provide formal definitions to clarify our conflict detection methodology:

**External Conflicts:**
Each recommendation pair (R_current, R_outdated) generates scenarios S_current and S_outdated, evaluated independently against current medical ground truth. External conflict occurs when:
- Model endorses S_outdated (should reject)
- Model rejects S_current (should endorse)

**Internal Conflicts:**
Assessed using paired scenarios where simultaneous endorsement indicates internal knowledge inconsistency:
- Given scenario pair (S_i,current, S_i,outdated) for concept i
- Internal conflict occurs when: Model(S_i,current) = Endorse AND Model(S_i,outdated) = Endorse
- IKCR quantifies frequency of such contradictions across all active pairs

### E.3 Analysis of Counterintuitive Scale Effects

Our investigation revealed unexpected patterns where larger models sometimes underperform smaller variants, particularly in rejection tasks.

**Empirical Evidence:**

| Model Family | Parameter Size | ECDA_rej Performance |
|--------------|----------------|---------------------|
| Qwen | 7B → 72B | 0.3540 → 0.2783 |
| LLaMA | 8B → 70B | 0.6256 → 0.5571 |
| Med42 | 8B → 70B | 0.5562 → 0.2811 |

**Proposed Mechanistic Explanation:**

We hypothesize this phenomenon results from **pre-training bias amplification**:

1. **Authority Signal Hypothesis**: Clinical scenarios rich with specialized medical terminology trigger strong "correctness" associations learned during pre-training.

2. **Scale-Dependent Bias**: Larger models, exposed to more diverse medical corpora, develop stronger heuristic associations between clinical language and authoritative content.

3. **Alignment Override**: These pre-training biases can override rejection capabilities acquired during RLHF/instruction tuning, particularly when presented with plausible-sounding incorrect recommendations.

4. **Parameter Space Effects**: Smaller models may be less affected due to:
   - Weaker initial biases from smaller training corpora
   - Proportionally greater impact of alignment training updates

This analysis suggests that medical LLM evaluation requires careful consideration of both capability scaling and bias amplification effects.

---

## F. Chain-of-Thought Prompting Analysis

### F.1 Theoretical Framework

Chain-of-thought (CoT) prompting represents a complementary approach to our mitigation strategies, with distinct advantages and limitations:

**Potential Benefits:**
- Enhanced inconsistency detection in larger models
- Explicit reasoning traces for clinical decision-making
- Synergistic effects when combined with high-quality RAG

**Fundamental Limitations:**
1. **Parametric Knowledge Dependency**: CoT cannot correct underlying flawed model knowledge; it can only work with the knowledge already embedded in model parameters.

2. **Context Length Constraints**: Complex clinical scenarios may exceed effective reasoning chain lengths, leading to "forgetting" of earlier reasoning steps.

3. **Prompt Engineering Challenges**: Designing universally effective CoT prompts for diverse clinical scenarios remains difficult.

**Our Complementary Approach:**
Our methodology focuses on **parametric knowledge injection** through DPO, which:
- Directly corrects model knowledge using the same knowledge base as RAG
- Creates synergistic effects when combined with retrieval
- Provides more fundamental reliability improvements than prompt-based scaffolding

**Integration Potential:**
CoT prompting could be integrated with our RoD framework for additional performance gains:
This represents a complementary rather than competing approach to knowledge conflict resolution.

### F.2 Empirical Considerations

While we did not systematically evaluate CoT prompting in this study, our framework provides the foundation for such investigation:

1. **DPO + RAG Foundation**: Our RoD approach provides enhanced parametric knowledge that could better support CoT reasoning.

2. **Evaluation Metrics**: Our IKCR and ECDA metrics could directly assess CoT effectiveness in reducing knowledge conflicts.

3. **Future Work**: Systematic investigation of CoT integration represents a promising research direction building on our foundational improvements.

---

## G. Quality Assurance and Reproducibility

### G.1 Dataset Quality Validation

We implemented comprehensive quality assurance measures to ensure benchmark reliability:

**Manual Review Protocol:**
- Sample size: 300 scenarios (7% of total dataset)
- Review criteria:
  1. **Fidelity**: Accurate representation of given medical advice in scenario
  2. **Realism**: Plausible real-world clinical interactions
  3. **Clarity**: Appropriate integration of cognitive factors without overwhelming core medical content

**Quality Assessment Results:**
- No major fidelity issues identified
- Medical advice faithfully represented in generated scenarios
- Cognitive factors appropriately integrated without systematic bias introduction

### G.2 Complete Experimental Configuration

**Standardized Generation Parameters:**
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Temperature | 0.1 | Consistent, deterministic outputs |
| Top-p | 0.9 | Balanced nucleus sampling |
| Max Tokens | 200 | Sufficient for clinical reasoning |
| Top-k | Not used | Simplified sampling strategy |

**RAG Configuration:**
- Knowledge base: 195 clinical recommendation pairs
- Retrieval method: Sentence-BERT with cosine similarity
- k=2 most relevant guidelines retrieved
- Recall rate: 92% on synthetic scenarios

**DPO Training Details:**
- Learning rate: 5e-5
- Batch size: 16
- Training objective: 100% accuracy on preference pairs
- Rationale: Ensure complete parametric knowledge memorization before scenario evaluation

### G.3 Data and Code Availability

To ensure full reproducibility, we commit to releasing:

1. **Complete Dataset**: All 4,290 scenarios with cognitive factors
2. **Source Code**: Evaluation pipelines, metric implementations, and training scripts
3. **Model Outputs**: Complete response logs for all evaluated models
4. **Analysis Code**: Statistical analysis and visualization scripts

All materials will be made publicly available to support research reproducibility and enable community validation of our findings.

---

## H. Future Research Directions

### H.1 Multi-Category Conflict Extension

Our current benchmark focuses on single-category modifications to maintain controlled difficulty. Future work could explore:

**Complex Guideline Evolution:**
- Scenarios where recommendations evolve across multiple categories simultaneously
- Real-world guideline tracking to validate synthetic conflict generation
- Temporal analysis of actual medical knowledge evolution patterns

### H.2 Broader Domain Coverage

Extension beyond diabetes and HIV to encompass:
- Cardiovascular medicine guidelines
- Cancer treatment protocols
- Psychiatric medication recommendations
- Emergency medicine decision trees

### H.3 Real-World Validation Studies

**Longitudinal Evaluation:**
- Tracking actual guideline updates over time
- Comparing synthetic conflicts with genuine medical knowledge evolution
- Healthcare worker validation of scenario realism and clinical relevance

**Clinical Integration Studies:**
- Pilot testing in controlled clinical education environments
- Assessment of LLM reliability in actual medical decision support contexts
- Integration with electronic health record systems for real-world evaluation

### H.4 Advanced Mitigation Strategies

**Temporal Knowledge Graphs:**
- Dynamic knowledge representation for evolving medical guidelines
- Graph-based conflict detection and resolution
- Automated knowledge base updating mechanisms

**Meta-Learning Approaches:**
- Few-shot adaptation to new medical domains
- Transfer learning across related medical specialties
- Continual learning frameworks for ongoing guideline evolution

