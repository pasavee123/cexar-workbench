CeXaR: Fidelity & Interpretation Research Manifest (Engineering Handoff Document)

1. บทวิเคราะห์และคัดกรองงานวิจัยเชิงกลยุทธ์ (Core Fidelity / Interpretation Papers)

ในฐานะ AI Research Lead เป้าหมายสูงสุดของ CeXaR คือการสร้างระบบอธิบายผลที่มีความซื่อตรงเชิงกลไก (Semantic Fidelity) ไม่ใช่เพียงแค่การสร้าง Heatmap ที่ดูสวยงามหรือ "ดูน่าเชื่อถือ" สำหรับมนุษย์ (Visual Plausibility) เราต้องเผชิญกับความเสี่ยงที่โมเดลจะใช้วิธี "เดาถูกจากเหตุผลที่ผิด" (Right for the wrong reasons) ผ่านกลไก "Combinatorial Shortcuts"

การคัดเลือก Papers ต่อไปนี้มุ่งเน้นที่การพิสูจน์ "Exclusivity" ของคำอธิบายตามหลักการของ Jain & Wallace (คำอธิบายต้องเป็นหนึ่งเดียวและเฉพาะเจาะจงต่อการตัดสินใจ) และการตรวจสอบความสมเหตุสมผลผ่าน Sanity Checks เพื่อคัดกรองวิธีการที่ให้ผลลัพธ์เป็นเพียง Noise ที่ดูเหมือนโครงสร้างวัตถุ (Artifacts) ออกไปจากระบบของเรา

ตารางวิจัยเชิงกลยุทธ์สำหรับ CeXaR

Method / Concept	Paper URL	Code URL	What it evaluates	CNN support	ViT support	Repro Score
ROAR (Hooker et al.)	https://arxiv.org/abs/1805.12241	https://github.com/google-research/google-research/tree/master/interpretability_benchmark	Fidelity via Retraining (Gold Standard)	Yes	Yes	High
Attention is not explanation (Jain & Wallace)	https://arxiv.org/abs/1902.10186	https://github.com/successar/AttentionExplanation	Exclusivity / Adversarial Attention	No	Yes	High
Attention is not not explanation (Wiegreffe & Pinter)	https://arxiv.org/abs/1908.04626	https://github.com/sarahwie/attention	Model-consistent Adversaries	No	Yes	High
Saliency map sanity checks (Adebayo et al.)	https://arxiv.org/abs/1810.03292	https://github.com/adebayoj/sanity_checks_saliency	Sensitivity to Weight/Label randomization	Yes	No	High
Combinatorial Shortcuts (Bai et al.)	https://doi.org/10.1145/3447548.3467307	Insufficient evidence	Extra info encoding in masks	No	Yes	Medium
Grad-ECLIP	Insufficient evidence	Insufficient evidence	N/A	N/A	N/A	Low


--------------------------------------------------------------------------------


2. กรอบการวัดผลความซื่อตรงของคำอธิบาย (Fidelity Metrics Hierarchy)

การวัดผลแบบ Deletion/Insertion แบบดั้งเดิม (No retraining) นั้นลวงตา เนื่องจากพิกเซลที่ถูกลบออกไปทำให้ข้อมูลหลุดจาก Distribution เดิม (Distribution Shift) จนโมเดลประสิทธิภาพตกเพราะ "ความแปลกปลอม" ไม่ใช่เพราะ "ความสำคัญ" ของข้อมูล ดังนั้น CeXaR จะใช้ ROAR (RemOve And Retrain) เป็นเกณฑ์หลัก แม้จะมีต้นทุนการคำนวณสูง (ต้อง Retrain อย่างน้อย 5 ครั้งต่อหนึ่งระดับการลบ) เพื่อความแม่นยำสูงสุดในงาน Chest X-ray ที่มี Noise สูง

ตาราง Metrics สำหรับการทำ Handoff

Metric	Purpose	How to calculate	Strength	Weakness	Evidence URL	Codex/Claude next step
ROAR	วัด Fidelity ที่แท้จริง	ลบพิกเซล t\% ตามค่าความสำคัญ แล้ว Retrain ใหม่จากศูนย์	ป้องกัน Distribution Shift	High cost (5x retrain per t)	https://arxiv.org/abs/1805.12241	Implement a loop to retrain ResNet-50 5 times for each t \in [10, 30, 50, 70, 90]
AOPC	วัดความไวของโมเดล	Area Over the Perturbation Curve ของค่า Confidence	คำนวณเร็ว	เสี่ยงต่อ Distribution Shift	https://arxiv.org/abs/2509.18913v1	Script to compute confidence decay without retraining for baseline comparison
Pointing Game	วัด Localization	จุด Saliency สูงสุดต้องอยู่ใน Bounding Box	เข้าใจง่ายเชิงคลินิก	ไม่มองภาพรวม Heatmap	https://arxiv.org/abs/2010.11929	Use Bbox from CheXlocalize to run hit/miss test
Sanity Checks	ตรวจสอบความบริสุทธิ์	รัน Weight และ Label Randomization	คัดกรอง Unfaithful Methods	เป็นเพียงเกณฑ์ขั้นต่ำ	https://arxiv.org/abs/1810.03292	Execute randomization on model parameters and compare SSIM of heatmaps
JSD	วัดความต่างของคำอธิบาย	Jensen-Shannon Divergence ระหว่าง Attention Maps	วัดความไม่เป็นหนึ่งเดียว	แปลผลเชิงการแพทย์ยาก	https://arxiv.org/abs/1902.10186	Compute JSD between base attention and adversarial attention in ViT


--------------------------------------------------------------------------------


3. การวิเคราะห์ความเสี่ยงและข้อจำกัดของวิธีการอธิบายผล (Risks of Explanation Methods)

เราต้องระวัง "Unfaithful Ensembles" และภาพที่ดูดีแต่โกหก (Visually Convincing but Unfaithful) โดยเฉพาะในกรณีของ "Combinatorial Shortcuts" ที่ Bai et al. เตือนว่าโมเดลอาจใช้ตำแหน่งของ Mask เป็นช่องทางในการส่งผ่านข้อมูล (Encoding) แทนที่จะใช้พิกเซลภาพจริง

Risk	Affected methods	Why it matters	Evidence URL	How to test in CeXaR
Combinatorial Shortcuts	Attention, Mask-based	โมเดลใช้โครงสร้างของ Mask ในการทำนายแทนพิกเซล	https://doi.org/10.1145/3447548.3467307	Apply "Random Attention Pretraining" and "Instance Weighting"
Adversarial Attention	Transformer Attribution	สร้างคำอธิบายที่ต่างกันสุดขั้วแต่ผลทำนายเท่าเดิม	https://arxiv.org/abs/1902.10186	Search for max-JSD attention with \epsilon-TVD output change
Randomization Failure	Grad-CAM (บางกรณี), Raw Gradient	Heatmap ไม่เปลี่ยนแม้ Label จะถูกสุ่มใหม่ (Label Randomization)	https://arxiv.org/abs/1810.03292	Perform cascades of layer-wise weight randomization
Model Modification Risk	Deletion (No-retrain)	ประสิทธิภาพตกเพราะ Artifacts จากการลบพิกเซล	https://arxiv.org/abs/1805.12241	Compare ROAR degradation curve vs. inference-time deletion


--------------------------------------------------------------------------------


4. ทรัพยากรข้อมูลและเกณฑ์มาตรฐานสำหรับการตรวจสอบ (Fidelity-Compatible Resources)

เพื่อให้การวัด Fidelity มี "Anchor" ที่เชื่อถือได้ เราต้องใช้ข้อมูลที่มี Expert-level annotations เท่านั้น

Dataset	Annotation type	Public?	URL	Diseases	Useful for CeXaR?	Notes
CheXlocalize	Bounding boxes / Pixel masks	Research	https://arxiv.org/abs/2010.11929	Pathologies in CXR	High (Primary Anchor)	Use for Localization Fidelity research only
MIMIC-III	ICD-9 Labels (Textual)	Yes	https://physionet.org/content/mimiciii/	ICU Data	Low (Contextual)	Warning: Primary labels are ICD-9 for NLP tasks, not vision-centric
ImageNet	Classification/Bbox	Yes	https://www.image-net.org/	General objects	Medium (Baseline)	Good for checking ROAR implementation logic


--------------------------------------------------------------------------------


5. วิธีการที่เหมาะสมสำหรับการปรับใช้ใน CeXaR (Methods Recommended for Implementation)

จากการวิจัยของ Hooker et al. วิธีการแบบ Single-pass ส่วนใหญ่ให้ผลลัพธ์ไม่ดีกว่า Random Baseline วิธีการที่พิสูจน์แล้วว่ามีความซื่อตรงสูงในระดับวิศวกรรมคือ Ensemble-based approaches

Method	Why useful	Difficulty	Required data	Compatible baselines	Risk
SmoothGrad-Squared	ดีกว่า Random Baseline อย่างชัดเจน (ต่างจาก Classic version)	Medium	CXR Images	ResNet-50 / CNN	Computational cost (multi-sampling)
VarGrad	ตรวจจับความแปรปรวนของคุณลักษณะ (Feature Variance) ได้ดี	Medium	CXR Images	CNN / ViT	ต้องการ Hyperparameter tuning (noise level)
Integrated Gradients	มีคุณสมบัติ Axiomatic (Completeness)	Medium	Baseline Image	ResNet / DenseNet	Baseline Sensitivity (Black vs Mean image)


--------------------------------------------------------------------------------


6. เทคโนโลยีที่ยังไม่พร้อมสำหรับการใช้งานทางคลินิก (Methods Not Ready Yet)

ทางทีมวิศวกรรมขอระงับการใช้งานวิธีต่อไปนี้ เนื่องจากล้มเหลวในการทดสอบ Sanity Checks หรือมีประสิทธิภาพต่ำกว่าเกณฑ์มาตรฐาน

Method	URL	Missing pieces	Why not ready
Raw Gradients	https://arxiv.org/abs/1312.6034	Noise reduction	ผลลัพธ์แย่กว่า Random Designation ในการทดสอบ ROAR
Classic SmoothGrad	https://arxiv.org/abs/1706.03825	Accuracy gain	Warning: เป็นภาระทางการคำนวณโดยไม่ให้ความแม่นยำเพิ่มขึ้น (Source 2)
Guided Backprop	https://arxiv.org/abs/1412.6806	Fidelity proof	ล้มเหลวในการทำ Label Randomization check (Adebayo et al.)


--------------------------------------------------------------------------------


7. แผนการตรวจสอบระบบด้วย Codex/Claude (Audit Plan)

วิศวกรต้องใช้ AI Assistant ในการรัน Audit ตามลำดับดังนี้:

Task	Target repo/file	Expected result	Pass/fail condition
Verify URL Integrity	Table in Section 1	All URLs must return HTTP 200/Source exists	Missing papers or 404 links
Inspect ROAR Logic	https://github.com/google-research/google-research/tree/master/interpretability_benchmark	Correct implementation of 5-run average retraining	Retraining not strictly separated from initialization
Sanity Check Execution	Internal ceXar/metrics/sanity.py	Heatmap changes significantly when labels/weights are randomized	SSIM > 0.9 after weight randomization (Fail)
Audit Shortcut Mitigation	Internal ceXar/models/vit_cxr.py	Inclusion of Random Attention Pretraining (Bai et al.)	Lack of mask-neutral learning implementation


--------------------------------------------------------------------------------


8. ข้อเสนอแนะการทดลองชุดแรกสำหรับ CeXaR (Recommended First Experiments)

Experiment 1: ROAR Baseline on Chest X-ray

* Objective: พิสูจน์ว่า SmoothGrad-Squared และ VarGrad ให้ผลดีกว่า Random Baseline ในโดเมน CXR จริงหรือไม่
* Reasoning: ข้อมูล CXR มีความซับซ้อนกว่า ImageNet (Source 2) เราต้องยืนยันว่า Metrics นี้ยังคง Valid
* Expected Insight: เส้นกราฟการลดลงของความแม่นยำ (Degradation curve) ที่ชันกว่า Random อย่างมีนัยสำคัญ

Experiment 2: Model-Consistent Adversary on ViT

* Objective: ค้นหา Adversarial Attention ที่มี JSD สูงแต่ TVD ต่ำ (ผลทำนายไม่เปลี่ยน) ในสถาปัตยกรรม ViT
* Reasoning: เพื่อระบุ "Degree of Freedom" ของ Attention ในการอธิบายโรคทรวงอก (Source 4)
* Expected Insight: ขอบเขตความเชื่อมั่น (Confidence bound) ของ Heatmap ที่แพทย์สามารถใช้ได้

Experiment 3: Integrated Gradients Baseline Sensitivity

* Objective: เปรียบเทียบผลลัพธ์ของ IG เมื่อใช้ "Black Image" เทียบกับ "Mean Image" เป็น Baseline
* Reasoning: Hooker et al. ระบุว่าการตั้งค่า (Configuration) มีผลอย่างมากต่อประสิทธิภาพของ Attribution
* Expected Insight: การเลือก Baseline ที่เหมาะสมที่สุดสำหรับภาพ X-ray ที่มี Dynamic range จำกัด


--------------------------------------------------------------------------------


9. รายการข้อกล่าวอ้างที่ยังไม่ได้รับการยืนยัน (Unverified Claims Monitor)

Claim	Missing evidence	What to verify next	Priority
"Attention equals importance"	ขัดแย้งกับหลักการ Adversarial Attention (Jain & Wallace)	ทดสอบ JSD บน CXR ViT	High
"Grad-CAM is clinical-ready"	ล้มเหลวในความไวต่อน้ำหนักโมเดลในบางงานวิจัย (Arun et al.)	รัน Adebayo Sanity Check บนโมเดลหลัก	High
"Heatmaps reduce diagnostic errors"	ขาดหลักฐานเชิงประจักษ์แบบ Human-in-the-loop	ออกแบบ User Study ร่วมกับรังสีแพทย์	Medium

Engineering Note: กระบวนการตรวจสอบ Fidelity ต้องทำแบบ Iterative ทุกครั้งที่มีการเปลี่ยน Model Weights หรือสถาปัตยกรรม ห้ามยึดถือผลการตรวจสอบเพียงครั้งเดียวเป็นที่สิ้นสุด (Source: xAI-CV)
