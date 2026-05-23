Heatmap Validation & Segmentation Support Manifest สำหรับ CeXaR

ในฐานะผู้เชี่ยวชาญอาวุโสด้านวิศวกรรม AI ทางการแพทย์ เอกสารฉบับนี้ถูกจัดทำขึ้นเพื่อกำหนดกรอบการทำงาน (Framework) และโปรโตคอลมาตรฐานในการส่งมอบงาน (Engineering Handoff) สำหรับการตรวจสอบความถูกต้องของระบบ Explainable AI (XAI) ในโครงการ CeXaR โดยมุ่งเน้นการเปลี่ยนนิยามของ "Visual Similarity" ให้กลายเป็น "Numerical Metric" ที่วัดผลได้จริงตามหลักวิศวกรรมซอฟต์แวร์ทางการแพทย์


--------------------------------------------------------------------------------


1. วิเคราะห์และคัดกรองชุดข้อมูลสำหรับการระบุตำแหน่ง (Chest X-ray Localization / Segmentation Datasets)

การเลือก Dataset สำหรับการ Validation จะต้องให้ความสำคัญกับคุณภาพของ Ground Truth (GT) โดยเฉพาะระดับความละเอียด (Granularity) เพื่อใช้เป็นบรรทัดฐาน (Gold Standard) ในการเปรียบเทียบกับ Heatmap ที่ AI สร้างขึ้น

การเปรียบเทียบชุดข้อมูลเชิงลึก

Dataset	Annotation type	Public?	URL	Pathologies	Format	Useful for CeXaR?	Notes
CheXlocalize	Pixel-level & Most-representative points	Yes	Link	10 Pathologies (Atelectasis, Cardiomegaly, Consolidation, Edema, Enlarged Cardiomediastinum, Lung Lesion, Lung Opacity, Pleural Effusion, Pneumothorax, Support Devices)	JSON / Pixel Mask	Highest	เป็น Gold Standard สำหรับการวัด IoU และ Pointing Game
VinDr-CXR	Bounding boxes (Local) & Global labels	Yes	Link	22 Local labels / 6 Global labels	DICOM / CSV	High	มี 18,000 images พร้อม labels จากรังสีแพทย์ 17 ท่าน
RSNA Pneumonia	Bounding boxes	Yes	Link	Pneumonia	DICOM / CSV	Medium	ข้อมูลเฉพาะทางสำหรับปอดอักเสบ
NIH Bounding Box	Bounding boxes	Yes	Repo Lead	Various pathologies	CSV	Medium	ควรตรวจสอบ "anshuak100" repo สำหรับอ้างอิงตำแหน่ง
CXLSeg	Automated masks	Yes	Link	Anatomical (Lung)	PNG	Low-Medium	ขนาด 243k images (MIMIC-based)
CheXmask	Automated masks	Yes	Link	Anatomical (Lung/Heart)	PNG	Low-Medium	ขนาดใหญ่กว่า CXLSeg (657k images) แต่เป็น Automated noise

การประเมินความเหมาะสม (So What?)

CheXlocalize ถูกเลือกเป็นเกณฑ์มาตรฐานอันดับหนึ่งสำหรับ CeXaR เนื่องจากมีข้อมูลครอบคลุมทั้ง 10 Pathologies สำคัญ และให้ข้อมูลในระดับ Pixel-level Segmentations ซึ่งเหนือกว่า "Weak Labels" หรือ Bounding Boxes ทั่วไป ช่วยให้สามารถคำนวณความแม่นยำเชิงพื้นที่ได้ในระดับสูงสุด


--------------------------------------------------------------------------------


2. การจำแนกและประเมินประเภทของคำสั่งประกอบภาพ (Annotation Types Evaluation)

ตารางเปรียบเทียบคุณลักษณะ

Annotation type	Example datasets	Strength	Weakness	Good for heatmap evaluation?
Pixel-level Segmentation	CheXlocalize, CXLSeg	ละเอียดที่สุด (Anatomical accuracy)	ต้นทุนการทำสูงมาก (High effort)	Excellent - สำหรับ IoU/Dice Validation
Bounding Boxes	VinDr-CXR, RSNA	ทำได้รวดเร็ว บอกตำแหน่งได้ชัดเจน	มักรวมพื้นที่ปกติ (Noise) เข้ามาใน Box	Good - สำหรับ Localization AUROC
Phrase Grounding	VinDr-CXR-VQA	ให้บริบทการให้เหตุผล (Clinical Reasoning)	ประเมินผลเชิงตัวเลขยาก	High - สำหรับการตรวจสอบความสอดคล้องของเหตุผล
Weak Labels	Image-level labels	ข้อมูลจำนวนมหาศาล (Big Data)	ไม่ระบุตำแหน่ง	Low - ไม่สามารถใช้ Validate Heatmap ได้โดยตรง

Analytical Layer: ในขณะที่ "Radiologist Points" เหมาะสมสำหรับการทดสอบ Pointing Game (วัดว่าจุดที่ Model สนใจที่สุดตรงกับจุดที่หมอชี้หรือไม่) แต่สำหรับ CeXaR เราต้องการ IoU Validation บน Pixel-level เพื่อยืนยันว่าขอบเขต (Extent) ของรอยโรคนั้นไม่ถูก AI คาดการณ์ผิดพลาดจนนำไปสู่การวินิจฉัยที่คลาดเคลื่อน


--------------------------------------------------------------------------------


3. มาตรวัดประสิทธิภาพสำหรับการระบุตำแหน่ง (Localization / Segmentation Metrics)

ตารางรายละเอียด Metrics

Metric	Purpose	Formula / Logic	Strength	Weakness	Evidence URL
IoU (Jaccard Index)	วัดความทับซ้อนเชิงพื้นที่	Area_{Overlap} / Area_{Union}	มาตรฐานสากลสำหรับ Segmentation	อ่อนไหวต่อ Threshold	Nature MI (2022)
Dice Score	วัดความคล้ายคลึงของพื้นที่	$2	A \cap B	/ (	A
Pointing Game	ตรวจสอบ Max Activation Point	Hit = P_{max} \in GT_{ROI}	ไม่ต้องการ GT ขอบเขตละเอียด	ไม่ตรวจสอบส่วนเกิน (Over-highlight)	IEEE TMI (2022)
Lung Attention Ratio (LAR)	วัดการโฟกัสภายในอวัยวะเป้าหมาย	\frac{\sum_{(x,y) \in \Omega_{lung}} A(x,y)}{\sum_{(x,y)} A(x,y)}	ตรวจจับ Background Noise ได้ดี	ต้องมี Anatomical Prior	arXiv:2511.00456

สูตรการคำนวณ LAR: LAR = \frac{\sum_{(x,y) \in \Omega_{lung}} A(x,y)}{\sum_{(x,y)} A(x,y)} หมายเหตุ: \Omega_{lung} ในที่นี้หมายถึง Coarse Anatomical Prior (ไม่ใช่ precise segmentation) เพื่อตรวจสอบว่า Focal Loss สามารถบีบให้ Model ไม่ไปสนใจ "Pseudo-RGB artifacts" หรือพื้นหลังที่เป็นสีดำนอกทรวงอก


--------------------------------------------------------------------------------


4. โปรโตคอลการตรวจสอบความถูกต้องของ Heatmap (Heatmap Evaluation Protocol)

ตารางขั้นตอนการปฏิบัติงาน (Handoff Workflow)

Step	Input	Output	Failure risk	Codex/Claude audit task
1. Alignment Check	DICOM (512x512)	Preprocessed Tensor	Spatial misalignment จากการ Resize	ตรวจสอบ Interpolation method (Bilinear vs Bicubic) ว่าไม่ทำให้พิกัดเคลื่อน
2. Heatmap Gen	Model Weights	Saliency Map	ViT Grid mismatch (16x16 patch)	คำนวณความละเอียดของ Feature Map เทียบกับ Input Resolution
3. Thresholding	Heatmap + \tau	Binary Mask	การเลือก \tau ที่ไม่เป็นกลาง (Bias)	วิเคราะห์ Intensity distribution เพื่อหา \tau ที่เหมาะสมอัตโนมัติ
4. Metric Audit	Binary Mask + GT	IoU / Dice	Wrong calculation logic	ตรวจสอบ JSON Schema สำหรับ gt_finding และ gt_location


--------------------------------------------------------------------------------


5. การวิเคราะห์ความเสี่ยงและกรณีที่อาจเกิดความล้มเหลว (Risks / Failure Cases)

Risk	Why it matters	Evidence	How to detect in CeXaR
Diagnostic Noise in GT	มนุษย์มีความผิดพลาดในการระบุตำแหน่ง	45% Decision Errors, 30% Search, 25% Recognition (Krupinski)	ใช้ C-Score เพื่อวัดความสอดคล้องระหว่าง Model หลายตัวเทียบกับ GT
Coarse ViT Maps	ความละเอียดต่ำเชิงพื้นที่	ViT-B/16 ประมวลผลแบบ 16x16 pixel patches	แจ้งเตือนเมื่อ Heatmap มีลักษณะเป็นตาราง (Grid artifacts) หยาบเกินไป
Technical Mismatch	ข้อมูลตำแหน่งเคลื่อน (Shift)	Spatial misalignment ใน Preprocessing pipeline	ตรวจสอบ Ratio ของ ROI หลังจาก Warp ภาพ


--------------------------------------------------------------------------------


6. วิธีการที่เหมาะสมสำหรับโครงการ CeXaR (Methods Suitable for CeXaR)

Method	Why useful	Required data	Compatible baselines	Difficulty	Risk
Grad-CAM Overlap	มาตรฐานสำหรับ CNNs	Pixel-level mask	ResNet, DenseNet	Low	ขาดความละเอียดในรอยโรคขนาดเล็ก
Segmentation Fidelity	ตรวจสอบความถูกต้องของขอบเขต	High-res masks	ทุกสถาปัตยกรรม	High	ใช้ทรัพยากรการคำนวณสูง
MobileNet-V3 Baseline	Optimal trade-off (4.9M params)	Image-level labels	MobileNet-V3	Low	Accuracy ต่ำกว่า ViT เล็กน้อย (96-98%)

Strategic Evaluation: การเลือก MobileNet-V3 (4.9M parameters) เป็น Baseline สำหรับ CeXaR เป็นกลยุทธ์ที่ชาญฉลาดเมื่อเทียบกับ ViT (86.2M parameters) เนื่องจากให้ประสิทธิภาพที่ยอมรับได้ในทรัพยากรที่จำกัด และให้ Heatmap ที่มีความละเอียด (Feature map density) สูงกว่าโครงสร้าง Patch-based ของ ViT


--------------------------------------------------------------------------------


7. แผนการตรวจสอบโดย Codex/Claude (Codex/Claude Audit Plan)

Task	Target	Expected result	Pass/fail condition
Schema Validation	dataset_config.json	JSON Schema ที่มี gt_finding และ gt_location	ต้องสอดคล้องกับมาตรฐาน VinDr-CXR-VQA
Interpolation Audit	preprocess.py	การใช้พิกัดคงที่หลังจากการ Resize	ห้ามมี Spatial Shift เกิน ±1 พิกเซล
IoU Logic Audit	metrics.py	การคำนวณ Intersection/Union ที่ถูกต้อง	ตรวจสอบ Zero Division Handling


--------------------------------------------------------------------------------


8. ข้อเสนอแนะสำหรับ Pipeline การตรวจสอบเครื่องแรก (Recommended First Validation Pipeline)

1. Baseline Model: ResNet-18 หรือ EfficientNet-B0 (เน้นความเสถียรของ Grad-CAM)
2. Dataset: CheXlocalize (เนื่องจากเป็นแหล่งข้อมูล Pixel-level GT ที่มีคุณภาพสูงสุด)
3. Explainability: Grad-CAM (เป็นมาตรฐานอุตสาหกรรมสำหรับ XAI ในปัจจุบัน)
4. Key Metric: ตั้งเป้าหมายที่ IoU @0.3 และ LAR > 0.6
5. Target Accuracy: 96–98% ตามเกณฑ์มาตรฐานของ ImageNet-pretrained models


--------------------------------------------------------------------------------


9. ประเด็นที่ยังไม่ได้รับการยืนยันและแผนงานในอนาคต (Unverified Claims)

Claim	Missing evidence	What to verify next	Priority
NIH Bounding Box URL	ไม่พบ Direct URL ใน Source หลัก	ตรวจสอบผ่าน GitHub "anshuak100/NIH-Chest-X-ray-Dataset"	High
LAR Robustness	ประสิทธิภาพ LAR ในโรคที่กระจายทั่วปอด	ทดสอบ LAR กับรอยโรคแบบ Diffuse เทียบกับ Focal	Medium
ViT Localization	วิธีแก้ปัญหา Coarse Map	ศึกษาการใช้ Transformer Attribution หรือ Higher resolution patches	Medium

Final Command: ให้นำ Manifest นี้เป็นกรอบอ้างอิงในการสร้าง Localization Validation Pipeline แรกของ CeXaR โดยใช้ CheXlocalize เป็นฐานข้อมูลหลักทันที
