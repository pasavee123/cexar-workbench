Failure Modes, Shortcut Learning, and Bias Manifest: คู่มือวิศวกรรมสำหรับโครงการ CeXaR

ในฐานะวิศวกรการเรียนรู้ของเครื่องทางการแพทย์และสถาปนิกข้อมูลอาวุโส เอกสารฉบับนี้ถูกจัดทำขึ้นเพื่อกำหนดกรอบการทำงานเชิงวิศวกรรม (Engineering Framework) ในการวิเคราะห์และป้องกันความล้มเหลวของแบบจำลองสำหรับโครงการ CeXaR เป้าหมายเชิงกลยุทธ์คือการสร้างระบบวินิจฉัยที่ไม่เพียงแต่มีประสิทธิภาพสูงในเชิงสถิติ แต่ต้องมีความโปร่งใส (Transparency) และความน่าเชื่อถือทางรังสีวิทยา (Radiological Reliability) โดยปราศจากการพึ่งพา "ทางลัด" หรืออคติที่ซ่อนอยู่ในชุดข้อมูล

1. บทวิเคราะห์โหมดความล้มเหลว (Failure Modes Analysis)

การระบุ Failure Modes เป็นหัวใจสำคัญของการทำ Failure Analysis เพื่อป้องกันการนำแบบจำลองที่ตัดสินใจบนพื้นฐานที่ผิดพลาด (Right for the wrong reasons) ไปใช้ในทางคลินิก หลักฐานเชิงประจักษ์พบว่าแบบจำลองมักมีพฤติกรรม "Source-Classification" หรือการแยกแยะแหล่งที่มาของชุดข้อมูลได้เกือบสมบูรณ์ (Near-perfect accuracy) แทนที่จะวิเคราะห์พยาธิสภาพจริง ซึ่งถือเป็นความล้มเหลวเชิงโครงสร้างที่ร้ายแรงที่สุด

Failure mode	Evidence URL	How it affects CXR AI	Risk to CeXaR	How to test
Shortcut Learning (Source Classification)	Exact URL not found in current sources	แบบจำลองจดจำคุณลักษณะเฉพาะของสถาบัน (เช่น ยี่ห้อเครื่องเอกซเรย์) จนทำนายแหล่งที่มาได้แม่นยำเกือบ 100%	ประสิทธิภาพจะลดลงทันทีเมื่อเผชิญกับข้อมูลจากสถาบันอื่น (External Dataset)	ทดสอบด้วย Source-Classification model เพื่อดูว่าโมเดลแยกแยะชุดข้อมูลต้นทางได้หรือไม่
Grad-CAM Artifact focus (Anatomical Violation)	Exact URL not found in current sources	Heatmap มักไฮไลท์นอกขอบเขตปอดหรือหัวใจ เนื่องจากข้อจำกัดของการทำ Interpolation จาก 14x14 feature maps สู่ภาพ 2000x2000	ความน่าเชื่อถือในการอธิบายผล (Interpretability) ต่ำ และอาจจับจ้องที่จุดสว่างที่สุดแทนรอยโรค	ประเมินด้วย Pointing Game และค่า mIoU เทียบกับ Radiologist Reference
External Validation Collapse	Exact URL not found in current sources	ประสิทธิภาพด้าน AUPRC และ F1-score ลดลงอย่างมีนัยสำคัญเมื่อทดสอบกับข้อมูลภายนอก (มากกว่า AUROC)	แบบจำลองขาด Generalizability ในระดับที่ใช้งานจริงไม่ได้	ทำ Cross-dataset validation และเน้นวัดผลด้วย AUPRC ในกลุ่มโรคที่มีความชุกต่ำ
Label Noise (Semantic Failure)	Exact URL not found in current sources	Rule-based labelers ล้มเหลวในการจัดการกับโครงสร้างประโยคปฏิเสธที่ซับซ้อน (Complex Negation) และคำสะกดผิด	Ground Truth ปนเปื้อน ทำให้โมเดลเรียนรู้ความสัมพันธ์ที่ผิดพลาดทางคลินิก	ตรวจสอบกรณี Negation (เช่น "no evidence of...") และคำสะกดผิด (เช่น "cariomegaly")

Failure Modes เหล่านี้มักถูกกระตุ้นโดย Dataset Shift ซึ่งเป็นปัจจัยพื้นฐานที่วิศวกรต้องควบคุมในส่วนถัดไป


--------------------------------------------------------------------------------


2. แหล่งที่มาและความเสี่ยงของการเปลี่ยนแปลงชุดข้อมูล (Dataset Shift Sources)

การเปลี่ยนแปลงแหล่งข้อมูล (Distribution Shift) ส่งผลโดยตรงต่อ Generalizability ของ CeXaR โดยเฉพาะเมื่อใช้ชุดข้อมูลสาธารณะที่มีมาตรฐานการติดฉลากและสัดส่วนประชากรที่ต่างกันอย่างสิ้นเชิง

Dataset	Shift type	Example issue	Evidence URL	Suggested evaluation
MIMIC-CXR / CheXpert	Institutional Bias	ข้อมูลมาจากศูนย์การแพทย์แห่งเดียว (Single-center cohort) ซึ่งมีโปรโตคอลการถ่ายภาพเฉพาะ	Exact URL not found in current sources	ทำ External validation และตรวจสอบประสิทธิภาพแยกตามประเภท View (AP/PA/Lateral)
NIH ChestX-ray14	Labeling Shift	การใช้อัลกอริทึม NLP รุ่นเก่า (NegBio) ในการติดฉลากอัตโนมัติซึ่งมีความคลาดเคลื่อนสูงกว่า CheXbert	Exact URL not found in current sources	เปรียบเทียบผลลัพธ์กับ Expert-validated labels ใน subset เล็กๆ
Demographic Shift	Population Bias	ความไม่สมดุลของสัดส่วนอายุและเพศ ซึ่งมักส่งผลให้โมเดลมีประสิทธิภาพต่ำในกลุ่มประชากรย่อย	Exact URL not found in current sources	ทำ Subgroup Performance Analysis โดยเน้น F1-score ในกลุ่มคนอายุน้อยและเพศหญิง

การตรวจจับ Shift เหล่านี้เป็นขั้นตอนเตรียมความพร้อมสำหรับ Shortcut Checklist เพื่อคัดกรองสัญญาณรบกวนที่โมเดลอาจนำไปใช้


--------------------------------------------------------------------------------


3. รายการตรวจสอบทางลัดและสิ่งแปลกปลอม (Shortcut / Artifact Checklist)

แบบจำลองคอมพิวเตอร์วิทัศน์มักหา "ทางลัด" (Shortcuts) จากสิ่งแปลกปลอมในภาพ (Artifacts) เพื่อทำนายผลลัพธ์โดยไม่พิจารณาคุณลักษณะทางคลินิก นี่คือจุดอ่อนสำคัญของสถาปัตยกรรม ViT และ CNN ที่ต้องได้รับการตรวจสอบ

Shortcut	How model may exploit it	Detection method	Codex/Claude audit task	Severity
Portable AP Marker	ใช้สัญลักษณ์เครื่องเคลื่อนที่เพื่อระบุสถานะผู้ป่วยวิกฤต (Bed-bound)	Correlation Analysis	ตรวจสอบความสัมพันธ์ระหว่าง 'Portable' tag กับการทำนายผล 'Edema' หรือ 'Effusion'	Critical
De-identification Masks	ร่องรอยการลบข้อมูล PHI (Black boxes) ถูกใช้เป็นตัวระบุแหล่งที่มาของข้อมูล	Saliency Map Overlay	ตรวจสอบว่า Heatmap มี Activation สูงในบริเวณ Masked area หรือไม่	High
14x14 Interpolation Artifacts	ความละเอียดต่ำของ Feature map ทำให้ Grad-CAM ไม่สามารถรักษาขอบเขตอวัยวะได้	Anatomical Boundary Check	ตรวจสอบอัตราส่วน Activation ภายนอก Lung/Heart mask เทียบกับภายใน	Medium
Text Markers (L/R)	การใช้ตำแหน่งตัวอักษรระบุท่าทางหรือสถาบันเป็นตัวบ่งชี้โรคแฝง	Metadata Confounding	ตรวจสอบว่าตำแหน่ง Text marker มีผลต่อการกระจายตัวของ Heatmap หรือไม่	High

ทางลัดเหล่านี้มักเกิดขึ้นควบคู่กับ Label Noise ซึ่งบิดเบือนสัญญาณที่แท้จริงของโรค


--------------------------------------------------------------------------------


4. ความไม่แน่นอนและสัญญาณรบกวนของฉลากข้อมูล (Label Noise / Uncertainty)

ความล้มเหลวของ Rule-based labelers (NegBio/CheXpert) ในการจัดการกับความคลุมเครือ (Uncertainty) และ Complex Negation เป็นปัจจัยเสี่ยงสำคัญ วิศวกรต้องเปลี่ยนมาใช้ Deep Learning labelers (CheXbert) และดำเนินการตรวจสอบเชิงคุณภาพ

Dataset	Label source	Noise risk	Recommended handling	Evidence URL	Audit task
MIMIC / CheXpert	Rule-based Labeler	ล้มเหลวในประโยคปฏิเสธซับซ้อน เช่น "no evidence of pneumothorax or bony fracture"	ใช้ CheXbert (BERT-based) ที่มีความเข้าใจเชิงความหมาย (Semantics) สูงกว่า	Exact URL not found in current sources	ตรวจสอบ Label 'Fracture' ในประโยคที่มีโครงสร้างปฏิเสธซับซ้อน
Public Datasets	NLP Pipeline	การสะกดผิดในรายงานรังสีวิทยา เช่น "cariomegaly", "mediastnium", "ateltasia"	นำกระบวนการ Backtranslation มาใช้เพื่อ Augmentation และสร้างความทนทานต่อคำผิด	Exact URL not found in current sources	ตรวจสอบความแม่นยำในการติดฉลาก 'Atelectasis' เมื่อพบคำว่า "ateltasia"

Label Noise ไม่เพียงแต่ลดประสิทธิภาพ แต่ยังสร้างอคติในระดับประชากรย่อยที่ต้องได้รับการวิเคราะห์เชิง Fairness


--------------------------------------------------------------------------------


5. อคติและความเท่าเทียมในแบบจำลอง (Bias / Fairness Analysis)

การลดทอนประสิทธิภาพในกลุ่มประชากรย่อย (Subgroup Performance Disparities) เป็นประเด็นทางยุทธศาสตร์ที่ CeXaR ต้องระวัง โดยเฉพาะอคติด้านอายุและเพศ

Bias type	Affected group/source	Evidence URL	Metric to check	Risk
Demographic Disparity	เพศหญิงและกลุ่มอายุน้อย	Exact URL not found in current sources	AUPRC และ F1-score ต่อกลุ่มประชากรย่อย	การวินิจฉัยพลาดในกลุ่มคนอายุน้อยที่อาจมีลักษณะพยาธิสภาพต่างจากค่าเฉลี่ย
Automation Bias	ผู้รังสีแพทย์รุ่นเยาว์	Exact URL not found in current sources	Acceptability rate / Over-reliance	การที่แพทย์เชื่อใจ Heatmap ที่ผิดพลาดจนละเลยพยาธิสภาพจริงในจุดอื่น
Imbalanced Pathology	โรคที่มีความชุก < 1% (เช่น Pleural Other)	Exact URL not found in current sources	Positive Predictive Value (PPV)	แบบจำลองมักทำนายพลาดในกลุ่มโรคหายากเนื่องจากข้อมูลฝึกสอนไม่เพียงพอ


--------------------------------------------------------------------------------


6. แผนการตรวจสอบสำหรับ Codex/Claude (Codex/Claude Audit Plan)

วิศวกรต้องใช้ Codex หรือ Claude ในการดำเนินการตรวจสอบตาม Engineering Acceptance Criterion (EAC) ต่อไปนี้

Task	Target data/code	Expected result	Engineering Acceptance Criterion (EAC)
Metadata Confounding Audit	CSV Metadata / Model weights	ตารางแสดงค่าสหสัมพันธ์ระหว่าง Confounders และโรค	Fail หากค่า Correlation ระหว่างเครื่องเอกซเรย์เฉพาะและโรคสูงเกิน 0.3
AUPRC Sensitivity Check	External Dataset	รายงานประสิทธิภาพแยกตามกลุ่มรอยโรค (Pathology-wise)	Fail หาก AUPRC ใน External set ลดลง > 15% เมื่อเทียบกับ Internal set
Anatomical Boundary Audit	Saliency Maps / Organ Masks	ค่าเฉลี่ย mIoU ภายในขอบเขตทางกายวิภาค	Fail หากค่า mIoU ของหัวใจและปอดต่ำกว่าเกณฑ์ Radiologist Reference


--------------------------------------------------------------------------------


7. การทดสอบความล้มเหลวระยะแรกที่แนะนำ (Recommended First Failure Tests)

จากการวิเคราะห์เชิงวิพากษ์ CeXaR ต้องดำเนินการทดสอบ 3 ประการนี้เป็นลำดับแรก:

1. Small Pathology Localization Gap Test (Lung Lesion): ทดสอบความสามารถในการระบุตำแหน่งรอยโรคขนาดเล็ก ข้อมูลจาก Saporta et al. ระบุว่า AI มีค่า mIoU เพียง 0.027 ซึ่งเป็นประสิทธิภาพที่แย่กว่าผู้เชี่ยวชาญถึง 93.6% ถือเป็นจุดที่เปราะบางที่สุด
2. Pneumothorax Hit Rate Challenge: ประเมินความแม่นยำในการชี้ตำแหน่ง (Pointing Game) ของโรคที่อันตรายถึงชีวิต เนื่องจาก AI มีช่องว่างประสิทธิภาพ (Hit rate gap) ถึง 60.4% เมื่อเทียบกับรังสีแพทย์ และมักจะล้มเหลวในกรณีที่มีรูปร่างซับซ้อน (Complexity/Elongation)
3. Support Devices Artifact Audit: ทดสอบว่าแบบจำลองใช้เครื่องมือแพทย์เป็นทางลัดหรือไม่ โดยเฉพาะอุปกรณ์ที่มีช่องว่างประสิทธิภาพสูงถึง 72.4% ในการระบุตำแหน่ง และมักเกิด interpolation artifacts จาก 14x14 feature maps สูงสุด


--------------------------------------------------------------------------------


8. ข้อกล่าวอ้างที่ยังไม่ได้รับการยืนยัน (Unverified Claims)

รายการเฝ้าระวังสำหรับทีมวิศวกร (Data Gaps) ที่ยังไม่พบหลักฐานยืนยันในแหล่งข้อมูลปัจจุบัน:

Claim	Missing evidence	What to verify next	Priority
Institutional Bias in Segmentation	ข้อมูลความแม่นยำของการ Segmentation ในภาพท่า AP	ตรวจสอบว่าภาพ AP view มีค่า RCA < 0.70 ในการสร้างมาสก์อวัยวะหรือไม่	High
Grad-ECLIP Advantage	ประสิทธิภาพเปรียบเทียบระหว่าง Grad-CAM และ Grad-ECLIP ใน CeXaR	ทำ Head-to-head comparison บนชุดข้อมูลภาษาไทยและภาษาอังกฤษ	High
Misspelling Robustness in ViT	ผลกระทบของคำสะกดผิด (ateltasia/mediastnium) ต่อการทำงานของ Attention heads	ทำการตรวจสอบ Attention weights เมื่อป้อนข้อความที่มีคำสะกดผิด	Medium

สรุป: รายงานฉบับนี้เป็น Engineering Handoff ที่เน้นการจัดการกับ Failure Modes และ Shortcuts อย่างเป็นระบบ เพื่อให้ CeXaR เป็นแบบจำลองที่ได้รับการรับรองมาตรฐานทางวิศวกรรมระดับสูงสุดก่อนนำไปทดสอบทางคลินิกจริง
