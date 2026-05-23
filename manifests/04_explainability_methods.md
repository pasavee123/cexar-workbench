Explainability Method Manifest สำหรับ CeXaR: Engineering Handoff Document

ในฐานะ Senior AI/ML Engineering Lead เอกสารฉบับนี้จัดทำขึ้นเพื่อกำหนดกรอบมาตรฐานวิศวกรรมในการใช้เทคนิค Explainable AI (XAI) สำหรับโครงการ CeXaR (Chest X-ray Analysis and Reasoning) จุดประสงค์หลักไม่ใช่เพียงการสร้าง Visualization แต่เป็นการสร้างระบบการตรวจสอบ (Auditability) ที่สามารถยืนยันได้ว่า Model ตัดสินใจจากพยาธิสภาพจริง ไม่ใช่จาก Confounders หรือ Artifacts ของฟิล์ม โดยอ้างอิงจากมาตรฐานงานวิจัยของ Saporta et al. (Stanford) และ Adebayo et al. (Google Brain)


--------------------------------------------------------------------------------


1. Standard Explainability Methods

การคัดเลือก XAI Method สำหรับงาน Chest X-ray (CXR) มีความท้าทายสูงเนื่องจากรอยโรคส่วนใหญ่มีการกระจายตัวแบบ Multilabel และต้องการความแม่นยำในการระบุตำแหน่ง (Localization) ที่สูงมาก เมื่อเทียบกับ Human Benchmark (รังสีแพทย์) เราจะแบ่งกลุ่มเทคนิคตามความสามารถในการผ่าน Sanity Checks และความเข้ากันได้กับสถาปัตยกรรม Model

ตารางสรุปมาตรฐาน Explainability Methods

Method	Paper URL	Code URL	CNN support	ViT support	Requires gradients?	Requires model modification?	Multi-label support	Repro Score
Grad-CAM	https://doi.org/10.48550/arXiv.1611.07450	https://github.com/jacobgil/pytorch-grad-cam	Yes	Yes	Yes	No	Yes	High (Passes Sanity Checks)
Integrated Gradients	https://doi.org/10.48550/arXiv.1703.01365	https://goo.gl/hBmhDt	Yes	Yes	Yes	No	Yes	High (Passes Sanity Checks)
Eigen-CAM	https://doi.org/10.48550/arXiv.2008.02312	https://github.com/jacobgil/pytorch-grad-cam	Yes	Yes	No	No	Yes	Medium (Principal Component)
DeepLIFT	https://doi.org/10.48550/arXiv.1704.02685	https://github.com/ankitkh/deeplift	Yes	No	Yes	Yes	Yes	Low (ReLU Invariance)
Guided Backprop	https://doi.org/10.48550/arXiv.1412.6806	Exact URL not found in current sources	Yes	No	Yes	No	Yes	Low (Fails Sanity Checks)
Occlusion	https://doi.org/10.1101/2021.02.28.21252634	Exact URL not found in current sources	Yes	Yes	No	No	Yes	Medium (Perturbation-based)

เงื่อนไขทางเทคนิคสำหรับการใช้ Transformer-based Models: ในการสร้าง Heatmap สำหรับ ViT และ Swin Transformer ทีม Engineering ต้องใช้ reshape_transform เพื่อเปลี่ยนค่า Activation ดังนี้:

* Vision Transformers (ViT): แปลงจาก Batch x 197 x 192 เป็น 14x14 spatial images (โดยตัด Class Token ตัวแรกออก เหลือ 196 patches)
* Swin Transformers: แปลงจาก Batch x 49 x 1024 เป็น 7x7 spatial images ตามโครงสร้าง Hierarchical Window ของสถาปัตยกรรม

สรุปเชิงวิศวกรรม: เทคนิคที่ใช้ Gradient-based (เช่น Grad-CAM) มีความเสี่ยงต่อการเกิด Gradient Saturation แต่สะท้อนการทำงานของ Model ได้ดีกว่าหากผ่านการตรวจสอบ ในขณะที่ Perturbation-based (เช่น Occlusion) แม้จะไม่ขึ้นกับโครงสร้างภายในแต่มี Computational Cost ที่สูงกว่ามากสำหรับการทำ Inference ในระดับ Production


--------------------------------------------------------------------------------


2. Methods Suitable for CeXaR

การเลือกวิธีเหล่านี้มุ่งเน้นที่ความเชื่อถือได้ทางคลินิก (Clinical Reliability) โดยเฉพาะผลการศึกษาของ Saporta et al. ที่พบว่า Grad-CAM ทำ Localization ในงาน CXR ได้ดีที่สุด และในบางกรณี เช่น "Consolidation" สามารถทำคะแนน mIoU สูงกว่ารังสีแพทย์ (Human Benchmark) ถึง 128.1%

ตารางประเมินวิธีที่แนะนำสำหรับ CeXaR

Method	Why useful for CeXaR	Expected output	Risk	Codex/Claude next step
Grad-CAM	Localization สูงสุดใน CXR Benchmarks (Saporta et al.)	Coarse Heatmap ระบุบริเวณรอยโรคหลัก	ไม่สามารถจับรายละเอียดขอบเขต (Geometric nuances) ของรอยโรคขนาดเล็กได้	"Implement Grad-CAM using the last convolutional layer of DenseNet121 and apply Otsu's thresholding."
Integrated Gradients	ผ่าน Model Parameter Randomization Test อย่างสมบูรณ์	Pixel-level attribution ที่มีความละเอียดสูง	อาจมี Visual Diffusion หรือ Noise สูง	"Implement Integrated Gradients with SmoothGrad (averaging over noisy copies) to reduce visual noise."

เหตุผลเชิงยุทธศาสตร์: เราเลือก Grad-CAM เป็นหลักเนื่องจากความสัมพันธ์เชิงบวกระหว่าง Model Confidence และ Localization Performance ส่วน Integrated Gradients จะใช้เป็น Fidelity Checker เพื่อยืนยันว่า Model ไม่ได้ตัดสินใจจากปัจจัยภายนอก


--------------------------------------------------------------------------------


3. Methods Not Recommended Yet

เราจะไม่ใช้เทคนิคที่ให้ผลลัพธ์ที่ "สวยงาม" แต่ล้มเหลวในการสะท้อนถึงการเรียนรู้จริงของ Model (Fidelity) เพื่อลดความเสี่ยงในการสร้างความเชื่อมั่นที่ผิดพลาด (False Trust)

ตารางวิธีที่ไม่แนะนำในระยะเริ่มต้น

Method	URL	Why not recommended now	Missing pieces
Guided Backpropagation	https://doi.org/10.48550/arXiv.1412.6806	ล้มเหลวในการทดสอบ Cascading Weight Randomization	ความไวต่อ Model Parameters (Sensitivity)
Guided Grad-CAM	https://doi.org/10.48550/arXiv.1611.07450	ผลลัพธ์ไม่เปลี่ยนแปลงแม้จะสุ่ม Weights ของ Model ใหม่	Fidelity ต่อการตัดสินใจของ Model จริง

ปรากฏการณ์ "Edge Detector": จากงานวิจัยของ Adebayo et al. พบว่า Guided Backprop และ Guided Grad-CAM ทำหน้าที่เพียงเป็น "เครื่องตรวจจับเส้นขอบ" (Edge Detector) ของภาพ Input เท่านั้น ซึ่งเป็นคุณสมบัติของสถาปัตยกรรม CNN (Prior) ไม่ใช่สิ่งที่ Model เรียนรู้ (Knowledge) ดังนั้นจึงไม่สามารถใช้เพื่ออธิบายการตัดสินใจของ Model ได้


--------------------------------------------------------------------------------


4. Fidelity / Trustworthiness Risks: "The So What? Layer"

ความล้มเหลวของ XAI ส่งผลโดยตรงต่อความปลอดภัยของผู้ป่วย หากเทคนิค XAI มี Fidelity ต่ำ รังสีแพทย์อาจเข้าใจผิดว่า Model ตรวจพบมะเร็งปอดจากก้อนเนื้อจริง ทั้งที่ในความเป็นจริง Model อาจตรวจจากตำแหน่งของท่อช่วยหายใจ (Support Devices)

ตารางความเสี่ยงด้านความน่าเชื่อถือ

Risk	Affected methods	Why it matters	Evidence URL	How to test in CeXaR
Small Pathologies Gap	Grad-CAM, All saliency	ประสิทธิภาพลดลงสูงสุดใน "Lung Lesion" (ต่ำกว่ามนุษย์ 76.2%)	https://doi.org/10.1101/2021.02.28.21252634	ใช้ mIoU และ Hit Rate บน true positive slice เท่านั้น
ReLU Invariance	\epsilon-LRP, DeepLIFT	ใน ReLU networks เทคนิคเหล่านี้เป็นเพียงค่า Input \odot Gradient	https://doi.org/10.48550/arXiv.1711.00867	ทำ Weight Randomization Test และวัดค่า SSIM
Model Modification Risk	Layer-wise Attribution	การเปลี่ยนโมเดลเพื่อให้ใช้ XAI ได้อาจลดประสิทธิภาพการทำนาย	https://doi.org/10.48550/arXiv.1711.00867	ทดสอบ Predictive Performance (AUROC) หลัง Modify
Attention \neq Explanation	ViT Attention Maps	ค่า Attention มักไม่สัมพันธ์กับความสำคัญเชิงทำนายใน CXR	Exact URL not found in current sources	ทำ Sensitivity analysis บน Spatial patches


--------------------------------------------------------------------------------


5. Compatibility With Baselines

การจับคู่เทคนิค XAI ให้เหมาะสมกับ Baseline Model ของ CeXaR เป็นกุญแจสำคัญสู่ความเสถียร

Baseline model	Compatible methods	Difficulty	Known issues
DenseNet121	Grad-CAM, IG	Low	Best-performing baseline สำหรับ Localization ใน CXR
ResNet152	Grad-CAM, IG	Low	Localization ต่ำกว่า DenseNet เล็กน้อยแต่เสถียรต่อ IG
ViT / Swin	Grad-CAM (Reshaped)	Medium	ข้อห้าม: ห้ามเลือก Target Layer หลัง Final Attention Block เพราะ Gradients จะเป็น 0
CheXzero	Insufficient evidence	High	ยังไม่มีหลักฐานความเข้ากันได้ในสถานะ Zero-shot
RAD-DINO	Insufficient evidence	High	ต้องการการทดสอบ Localization Accuracy เพิ่มเติม


--------------------------------------------------------------------------------


6. Heatmap Output Standard

เพื่อให้เกิด Traceability และสามารถทำ Audit ย้อนหลังได้ ทุกผลลัพธ์ของ XAI ต้องถูกบันทึกตามมาตรฐานนี้

Output type	Required?	Format	Recommended save path	Notes
Raw Heatmap	Yes	NPY (Float32)	/outputs/xai/raw/	ห้าม Normalize เพื่อใช้ในการวิเคราะห์ Logit distribution
Overlay Image	Yes	PNG (RGBA)	/outputs/xai/overlay/	ใช้ Jet colormap ซ้อนบนต้นฉบับ CXR
Metadata JSON	Yes	JSON	/outputs/xai/meta/	บันทึก Model version, Threshold value (Otsu), และ AUROC


--------------------------------------------------------------------------------


7. Codex/Claude Audit Plan

เพื่อให้มั่นใจว่า Implementation ถูกต้องตามหลักการของ Adebayo et al. ให้ใช้ขั้นตอนการตรวจสอบดังนี้:

Task	Target repo/file	Expected result	Pass/fail condition
Weight Randomization	xai_engine.py	Heatmap ต้องเปลี่ยนสภาพอย่างสมบูรณ์เมื่อสุ่มน้ำหนักใหม่	Pass: SSIM < 0.5 เทียบกับของเดิม
Label Randomization	train.py	โมเดลที่เทรนด้วยฉลากปลอมต้องให้ Heatmap ที่ไร้ความหมาย	Pass: Rank Correlation เข้าใกล้ 0
ViT/Swin Shape Audit	transformers_cam.py	ตรวจสอบการใช้ reshape_transform ตามขนาด Patch	Pass: Output 2D spatial tensor (14x14 หรือ 7x7)


--------------------------------------------------------------------------------


8. Recommended First 3 Methods for CeXaR

เราจัดลำดับความสำคัญ (Prioritization) ตามหลักฐานความสำเร็จในการ Benchmark และความเสถียร:

1. Grad-CAM: วิธีหลักเนื่องจากผลการทดสอบ Localization mIoU สูงที่สุดในงานวิจัย CXR และมีความเสถียรต่อโครงสร้าง DenseNet121 ที่เป็นกระดูกสันหลังของ CeXaR
2. Integrated Gradients: เพื่อเป็นเครื่องมือตรวจสอบ Fidelity โดยต้อง Implement คู่กับ SmoothGrad เพื่อกำจัด Visual artifacts และ Noise ในระดับ Pixel
3. Eigen-CAM: แนะนำให้ใช้เป็น "Sanity Check" พื้นฐาน เนื่องจากเป็นค่า Principal Component (PC1) ของ Activation map โดยไม่ใช้ Gradients ทำให้เป็นอิสระจากปัญหา Gradient Saturation และ Artifacts จากการคำนวณอนุพันธ์

Radiology Insight: วิธีเหล่านี้จะช่วยระบุจุดที่ Model พบรอยโรค เช่น Pleural Effusion หรือ Cardiomegaly ได้อย่างแม่นยำเทียบเท่ากับรังสีแพทย์ (ยกเว้นรอยโรคขนาดเล็กที่ยังต้องระวังเป็นพิเศษ)


--------------------------------------------------------------------------------


9. Unverified Claims

ประเด็นที่ข้อมูลใน Source Context ยังไม่เพียงพอและต้องการการตรวจสอบเพิ่มเติม:

Claim	Missing evidence	What to verify next	Priority
XAI for CheXzero	ขาดข้อมูลการทดสอบ Localization กับ Zero-shot Multimodal models	ออกแบบการทดลองบน CheXlocalize dataset	Critical
Clinical Decision Speed	ยังไม่มีหลักฐานว่า Heatmap ช่วยให้หมอวินิจฉัยเร็วขึ้นจริงหรือไม่	ทำ User Study (Time-to-diagnosis)	Medium
Noise Sensitivity	ผลกระทบของภาพคุณภาพต่ำต่อความเสถียรของ XAI	ทดสอบด้วย Gaussian Noise injection	Low

คำสั่งสุดท้ายถึง Codex/Claude: "เริ่มดำเนินการสร้าง Prototype สำหรับ Grad-CAM และ Integrated Gradients (พร้อม SmoothGrad) บน DenseNet121 ทันที โดยต้องผ่าน Weight Randomization Test ก่อนเริ่มกระบวนการ Clinical Evaluation"
