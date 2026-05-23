CeXaR Research Idea & Experiment Roadmap Manifesto

1. High-priority Research Ideas: การยกระดับความน่าเชื่อถือด้วย XAI และ Metrics ยุคใหม่

Analytical Intro: ในฐานะ Senior AI Research Lead เป้าหมายสูงสุดของโครงการ CeXaR คือการก้าวข้ามผ่านเพียงแค่การวัดค่า Classification Accuracy ไปสู่การพิสูจน์ "Pixel-level Fidelity" เพื่อความปลอดภัยทางการแพทย์ (Clinical Safety) ข้อมูลจาก CheXlocalize และ Grad-ECLIP ชี้ให้เห็นว่าโมเดล CLIP แบบดั้งเดิมมักเกิดปัญหา "Sparse Attention" และ "Sparse Matching" ทำให้การระบุพยาธิสภาพผิดเพี้ยนไปจากความจริง (เช่น การระบุ 'Lobe' แทนที่จะเป็น 'Opacity' ที่ระบุใน Text) เราจึงต้องใช้แนวทาง Grad-ECLIP เพื่อวิเคราะห์ความสัมพันธ์ระหว่าง Matching Similarity และ Intermediate Spatial Features เพื่อสร้างความเชื่อมั่นให้กับรังสีแพทย์

Research Ideas Table:

Idea	Research question	Evidence URL	Baseline to compare	Required data	Required code	Metric	Expected output	Novelty	Difficulty	Risk
Fidelity-aware Heatmap Evaluation	วิธีการ XAI ใดที่ให้ค่า IMD สูงสุดในภาพ X-ray ทรวงอก?	https://github.com/Cyang-Zhao/Grad-Eclip	Grad-CAM (Penultimate layer), Rollout, GAME	CheXlocalize (Validation/Test)	Grad-ECLIP official repo	Deletion/Insertion AUC, IMD	Heatmap ที่สะท้อนพยาธิสภาพจริง (Fidelity)	การพิสูจน์ Grad-ECLIP ในโดเมน CXR	Medium	Low
Saliency Benchmarking for 10 Pathologies	โมเดลระบุตำแหน่งโรค 10 ชนิดได้แม่นยำเทียบเท่ารังสีแพทย์หรือไม่?	https://github.com/rajpurkarlab/cheXlocalize	Board-certified radiologist annotations	CheXlocalize (668 test images)	CheXlocalize benchmarking code	Point Game (PG), maskIoU, AP	Benchmark report เทียบโมเดล vs แพทย์	Pixel-level validation บน 10 โรคหลัก	High	Medium
ViT vs CNN Explainability Analysis	สถาปัตยกรรม ViT แก้ไขปัญหา Sparse Attention ได้ดีกว่า CNN หรือไม่?	https://doi.org/10.1038/s42256-022-00536-x	ResNet-50 CLIP, ViT-B/16	CheXpert / CheXlocalize	ViT and CNN-based CLIP models	energy-PG, Pixel Accuracy	รายงานการวิเคราะห์ Layer-wise gradients	การเปรียบเทียบ Fidelity ข้ามสถาปัตยกรรม	Medium	Low

Note on Scope: การทดลองทั้งหมดจะครอบคลุมพยาธิสภาพ 10 ชนิดจาก CheXlocalize ได้แก่: Atelectasis, Cardiomegaly, Consolidation, Edema, Enlarged Cardiomediastinum, Lung Lesion, Lung Opacity, Pleural Effusion, Pneumothorax, และ Support Devices.

Connectivity: ข้อมูลจากการเปรียบเทียบในส่วนนี้จะถูกใช้เป็นเกณฑ์ตัดสินใจว่าไอเดียใดควรถูกนำไปพัฒนาเป็น Experiment Candidate ในลำดับถัดไป โดยเน้นที่ไอเดียที่ให้ค่า IMD สูงที่สุด


--------------------------------------------------------------------------------


2. Experiment Candidates: แผนผังการทดสอบสมมติฐานเชิงเทคนิค

Analytical Intro: เพื่อลดช่องว่างระหว่างทฤษฎีและการประยุกต์ใช้จริง เราจะเน้นที่การตั้งสมมติฐานที่วัดผลได้ (Testable Hypotheses) โดยเฉพาะการพิสูจน์ว่า Grad-ECLIP สามารถแก้ปัญหาความล้มเหลวของ Grad-CAM ใน CLIP (ซึ่งขาด Gradients ใน Patch tokens ของชั้นสุดท้าย) ได้จริงหรือไม่ ผ่านการคำนวณ Gradient ของ Matching Score S เทียบกับ Attention layer output (o_{cls})

Experiment Candidates Table:

Experiment	Hypothesis	Method	Dataset	Baseline	Metric	Pass condition	Codex/Claude task
Fidelity Perturbation Test	Grad-ECLIP จะมีค่า IMD สูงกว่า Grad-CAM อย่างน้อย 15%	Deletion/Insertion step-by-step (0.5% pixels)	ImageNet-S / CheXlocalize	Grad-CAM (w.r.t. Penultimate layer)	IMD (Insertion Minus Deletion)	IMD > Baseline AND p-value < 0.05	Implement deletion script using torch.autograd.grad for S_T w.r.t o_{cls}
Pathology Localization Check	0-1 Normalization (Loosened Attention) จะลด False Positives นอกรอยโรค	Comparison of Softmax vs. 0-1 Normalization spatial weights	CheXlocalize (10 pathologies)	Softmax attention	Point Game (PG) Accuracy, maskIoU	PG Accuracy > 0.85 สำหรับรอยโรคขนาดใหญ่	Implement Loosened Attention map (\Phi) in Grad-ECLIP wrapper
Text-Specific Saliency Audit	คำระบุตำแหน่ง (e.g., "Pleural Effusion") จะให้ Heatmap ที่แม่นยำกว่า General words	Cross-modal gradient mapping	MSCXR	Raw self-attention	Word Importance score	Word Importance สูงสุดตรงกับรอยโรคในภาพ	Develop text-to-image correlation logger for specific pathologies

Connectivity: ผลลัพธ์เชิงตัวเลขจากการทดลองเหล่านี้จะเป็น "Hard Dependency" สำหรับการเลือกสถาปัตยกรรมของโมเดล CeXaR รุ่นถัดไป โดยเฉพาะการยืนยันประสิทธิภาพของ Loosened Attention


--------------------------------------------------------------------------------


3. Ideas Not Ready Yet: การวิเคราะห์อุปสรรคและสิ่งที่ต้องจัดเตรียม

Analytical Intro: การบริหารจัดการทรัพยากรต้องเป็นไปอย่างระมัดระวัง ไอเดียที่ยังขาดโครงสร้างพื้นฐานเชิงเทคนิคที่เสถียรจะถูกจัดอยู่ในหมวดเฝ้าระวังเพื่อไม่ให้กระทบต่อ Timeline หลัก

Gap Analysis Table:

Idea	Why not ready	Missing data/code/source	What to prepare first
ALBEF Style Cross-Attention XAI	Grad-ECLIP ปัจจุบันเน้น Dual-encoder เท่านั้น	Source code สำหรับ Cross-attention fusion layer gradient	วิจัยการขยาย Linear approximation ไปยัง Fusion layers
Real-time Clinical Integration	ความเร็วของ Grad-ECLIP ในระดับ Batch processing ยังไม่ถูกทดสอบ	Benchmarking data ในสภาพแวดล้อม High-throughput	ทดสอบ Processing time (s/img) เทียบกับ Grad-CAM (Target < 0.02s)
Abstract Concept Grounding	CLIP ล้มเหลวในการเข้าใจ "Comparative Attributes"	Insufficient evidence (Source ระบุว่า CLIP อ่อนด้านตำแหน่งเปรียบเทียบ)	ต้องทำ Fine-grained fine-tuning ด้วย Attribute-heavy captions ก่อน

Connectivity: เมื่อเราสามารถปลดล็อกปัญหาด้าน Code สำหรับ Fusion layer ได้ ไอเดียเหล่านี้จะถูกขยับขึ้นมาเป็น Experiment Candidates ทันที


--------------------------------------------------------------------------------


4. Required Resources: คลังทรัพยากรและแหล่งอ้างอิงสำหรับการวิจัย

Analytical Intro: ความพร้อมของข้อมูลคือรากฐานของความแม่นยำทางวิศวกรรม ทรัพยากรด้านล่างนี้ต้องถูกเข้าถึงและติดตั้งใน Environment ก่อนเริ่มการทดสอบ

Resource Directory Table:

Resource	URL	Needed for which idea	Status	Risk
CheXlocalize Dataset DOI	https://doi.org/10.71718/hap9-kn94	Saliency benchmarking (10 pathologies)	Available	Low
Grad-ECLIP Official Repo	https://github.com/Cyang-Zhao/Grad-Eclip	Fidelity evaluation (IMD implementation)	Available	Low
Nature Machine Intelligence Paper	https://doi.org/10.1038/s42256-022-00536-x	Methodology verification (Saliency benchmarking)	Available	Low
CheXlocalize GitHub (Official)	https://github.com/rajpurkarlab/cheXlocalize	Benchmarking code implementation	Available	Low
Canonical URL for Dataset	https://stanford.redivis.com/datasets/efx9-5nspnbb4b	Full data access and license terms	Available	Low

Connectivity: แหล่งข้อมูลทั้ง 5 จะถูกเรียกใช้โดยอัตโนมัติผ่าน Action Plan เพื่อเริ่มรันการทดลองลำดับความสำคัญสูง 3 รายการแรก


--------------------------------------------------------------------------------


5. Recommended First 3 Experiments: การเริ่มดำเนินการที่คุ้มค่าที่สุด (Quick Wins)

Analytical Intro: เพื่อสร้างความมั่นใจในระยะเริ่มต้น (Quick Wins) เราจะใช้กลยุทธ์ "Baseline-first" โดยเน้นการทำซ้ำ (Reproducibility) บนชุดข้อมูลมาตรฐาน

Ranked Recommendations:

1. Benchmarking Grad-ECLIP on CheXlocalize Validation Set:
  * เหตุผล: ใช้ Ground-truth จาก Board-certified radiologists เพื่อพิสูจน์ประสิทธิภาพของ Grad-ECLIP ในการระบุตำแหน่งโรค 10 ชนิด (เช่น Atelectasis, Pneumothorax)
2. Implementation of IMD Metric for CXR Models:
  * เหตุผล: เพื่อสร้างเกณฑ์มาตรฐาน (Fidelity metric) ที่เชื่อถือได้ในการวัดว่าการลบจุดที่เป็น "Opacity" ออก ส่งผลให้คะแนนโมเดลลดลงจริงหรือไม่
3. Comparative Analysis of Grad-CAM Penultimate vs. Grad-ECLIP:
  * เหตุผล: เพื่อพิสูจน์ข้อจำกัดของ Grad-CAM ในสถาปัตยกรรม CLIP และยืนยันความจำเป็นในการใช้ Gradient-based approach แบบใหม่

Connectivity: ผลลัพธ์จาก 3 ขั้นตอนนี้จะถูกส่งต่อไปยัง Action Plan เพื่อให้นักพัฒนาเขียน Code และรันโมเดลจริง


--------------------------------------------------------------------------------


6. Codex/Claude Action Plan: รายการปฏิบัติงานสำหรับวิศวกร AI

Analytical Intro: คู่มือการสั่งงานนี้ถูกย่อยให้อยู่ในระดับ Engineering Specification เพื่อให้นักพัฒนาหรือ AI Agent สามารถเขียนโค้ดได้ทันที โดยเน้นที่การคำนวณทางคณิตศาสตร์ที่ถูกต้อง

Action Plan Table:

Task	Target repo/file	Expected output	Pass/fail condition
Implement w_c Calculation	src/xai/grad_eclip.py	Python function using torch.autograd.grad for matching score S w.r.t. o_{cls} tokens	w_c matches the dimensionality of feature channels (C=512 or 768)
Loosened Attention Wrapper	src/xai/spatial_weights.py	Implementation of 0-1 Normalization for attention map \lambda_i = \Phi(q_{cls}k_i^\mathsf{T})	All spatial weights \lambda_i \in [0, 1] (not sparse like Softmax)
Upsampling Module	src/utils/heatmap.py	Bilinear interpolation of 14 \times 14 or 7 \times 7 heatmaps to 224 \times 224	Heatmap overlay aligned with original image resolution
Batch Fidelity Evaluation	scripts/eval_imd.py	Automated script for Deletion/Insertion AUC at 0.5% increments	Completion of 100 steps without memory overflow
Pathology-specific Report	outputs/reports/10_pathologies.csv	CSV reporting PG Accuracy and IMD for each of the 10 pathologies	All 10 pathologies listed in CheXlocalize are evaluated

Connectivity: Action Plan นี้จะเปลี่ยน Manifesto ให้กลายเป็นระบบที่ทำงานได้จริง และผลลัพธ์จะนำไปสู่การระบุประเด็นที่ต้องตรวจสอบเพิ่มเติมในส่วนสุดท้าย


--------------------------------------------------------------------------------


7. Unverified Claims: การเฝ้าระวังและประเด็นที่ต้องตรวจสอบเพิ่มเติม

Analytical Intro: ในโดเมนการแพทย์ เราต้องระมัดระวังประเด็นที่ยังขาดหลักฐานเชิงประจักษ์ โดยเฉพาะความสามารถของ CLIP ในการประมวลผลข้อมูลที่มีความซับซ้อนเชิงตำแหน่ง

Verification Table:

Claim	Missing evidence	What to verify next	Priority
Comparative Attribute Reliability	ขาดหลักฐานว่า Grad-ECLIP สามารถแก้ปัญหา "Size/Position" (e.g., "Left-side effusion") ได้	ทดสอบ Text-specific heatmaps บนคำระบุตำแหน่งเชิงเปรียบเทียบ	Critical High
ViT vs. SOTA CNN on Large CXR	ประสิทธิภาพของ ViT เมื่อเทียบกับ SOTA CNNs บนชุดข้อมูล CheXpert ขนาดใหญ่	รันการทดสอบข้ามสถาปัตยกรรมบน 200,000+ ภาพ	High
Device-agnostic Saliency	ความเสถียรของ Heatmaps เมื่อใช้ภาพจากเครื่อง X-ray ต่างยี่ห้อ (Scanner bias)	ทดสอบความเสถียรของ Grad-ECLIP ข้าม Dataset ภายนอก	Medium

Concluding Statement: Manifesto นี้คือคำสั่งปฏิบัติการที่สมบูรณ์สำหรับโครงการ CeXaR ขอให้ทีมวิศวกรและ AI Agents เริ่มดำเนินการตาม Action Plan ใน Section 6 ทันที เพื่อสร้างระบบ AI ทางการแพทย์ที่อธิบายได้และน่าเชื่อถือในระดับสูงสุด
