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

---

## I. Figure Legend

![Legend](assets/legend.png)

**Figure Legend**: Comprehensive legend for all performance visualization figures (Figures D1-D8). This legend applies to all bar charts showing model performance across cognitive factors and clinical change types, with consistent color coding for model identification and metric interpretation guidelines.

---

*These supplementary materials provide comprehensive additional details addressing all reviewer concerns and establishing the foundation for future research in medical knowledge conflict resolution.*
