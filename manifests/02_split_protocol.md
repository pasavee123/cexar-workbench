Technical Evaluation Protocol Manifest สำหรับ CeXaR

ในฐานะ Senior AI Research Engineer และ Medical Imaging Lead ความน่าเชื่อถือเชิงคลินิกของโมเดล Deep Learning ไม่ได้ขึ้นอยู่กับค่าความแม่นยำเพียงอย่างเดียว แต่หัวใจสำคัญคือ "การควบคุมสภาวะการทดลอง" (Experimental Control) หากสภาวะการทดลองไม่รัดกุม โมเดลจะเรียนรู้ "ทางลัด" (Shortcut Learning) เช่น การจดจำลักษณะทางเทคนิคของเครื่องสแกนหรือโครงสร้างกระดูกที่เป็นเอกลักษณ์เฉพาะตัวแทนที่จะเป็นพยาธิสภาพจริง เอกสารฉบับนี้กำหนดโปรโตคอลมาตรฐานเพื่อป้องกันข้อผิดพลาดเชิงเทคนิคและรับประกันความสามารถในการทำซ้ำ (Reproducibility) สำหรับโปรเจกต์ CeXaR โดยยึดหลักฐานจาก NIH ChestX-ray14 Evaluation Protocol และงานวิจัยที่เกี่ยวข้องเป็นบรรทัดฐาน


--------------------------------------------------------------------------------


1. กฎเกณฑ์การประเมินที่ต้องปฏิบัติตาม (Must-follow Evaluation Rules)

เพื่อให้มั่นใจว่าผลลัพธ์จาก CeXaR มีความโปร่งใสและเทียบเท่ามาตรฐานสากล ทุกการทดลองต้องปฏิบัติตามกฎเกณฑ์ดังต่อไปนี้:

Rule	Why it matters	Evidence URL (Plain Text)	Audit Task	Severity
Patient-level split	ป้องกัน Identity Leakage; Siamese networks สามารถระบุตัวตนผู้ป่วยจากฟิล์มได้ด้วย AUROC สูงถึง 0.9940 แม้เวลาผ่านไป 10 ปี	https://pmc.ncbi.nlm.nih.gov/articles/PMC9434540/	ตรวจสอบคำสั่ง intersection() ของ Patient ID ระหว่างชุดข้อมูลต้องเป็นเซตว่าง	Critical
No patient overlap	การปนเปื้อนของผู้ป่วย 67.4% ใน Official split ดั้งเดิมทำให้ค่า AUROC พุ่งสูงอย่างไม่เป็นธรรม (Identity shortcut)	https://laurenoakdenrayner.com/2018/01/24/chexnet-an-in-depth-review/	ยืนยันว่าไม่มี Patient ID เดียวกันปรากฏในทั้ง Train, Val และ Test	Critical
Preprocessing consistency	การคำนวณค่าสถิติแบบ Global ทำให้ข้อมูลจาก Test set รั่วไหลเข้าสู่ Training loop (Data Contamination)	https://www.reddit.com/r/MachineLearning/comments/1iu5cgg/r_why_is_there_mixed_views_on_how_traintestval/	ตรวจสอบว่า Mean/Std ถูกฟิต (fit) เฉพาะจาก Training set เท่านั้น	High
Correct label order	การเรียงลำดับ Label ผิดพลาดจะทำให้การคำนวณ Loss และ AUROC ไร้ความหมายเชิงคลินิก	https://huggingface.co/datasets/alkzar90/NIH-Chest-X-ray-dataset	ยืนยันการเรียงลำดับ 14 Pathologies ตามมาตรฐาน NIH (Atelectasis ถึง Pneumothorax)	High
AUROC Metrics Reporting	ป้องกันอคติจาก Class Imbalance (Hernia 0.2% vs Infiltration 17.8%) โดยต้องรายงานทั้ง Per-label และ Macro AUROC	https://arxiv.org/pdf/1905.06362	ตรวจสอบการรายงานผลเฉลี่ยแบบไม่ถ่วงน้ำหนัก (Unweighted Average)	Medium
Frozen Threshold	การปรับ Threshold บน Test set ทำให้เกิด Optimistic bias; ต้องแช่แข็งค่าที่ได้จาก Validation set	https://www.mdpi.com/2075-4418/16/8/1227/review_report	บังคับใช้ Threshold ที่คำนวณจาก Youden's J index บน Validation set เท่านั้น	High
CSV Alignment	ป้องกันการสลับ Index ระหว่างไฟล์ Prediction และ Ground Truth ซึ่งจะทำให้ผลประเมินผิดพลาด	https://www.kaggle.com/code/adamjgoren/nih-chest-x-ray-multi-classification	ทำการ Synchronization check ระหว่าง Image ID และ Prediction Index	Critical

ความล้มเหลวในการปฏิบัติตามกฎเหล่านี้จะนำไปสู่ความเชื่อมั่นที่ผิดพลาด (False Confidence) ซึ่งส่งผลโดยตรงต่อความปลอดภัยของผู้ป่วยเมื่อนำโมเดลไปใช้จริงในแผนกการแบ่งชุดข้อมูล


--------------------------------------------------------------------------------


2. โปรโตคอลการแบ่งชุดข้อมูล (Dataset Split Protocol)

การแบ่งข้อมูลแบบ Image-level ดั้งเดิมมีจุดอ่อนร้ายแรงคือโมเดลสามารถจดจำ "Trajectory" หรือประวัติการรักษาของผู้ป่วยรายเดิมได้ CeXaR จึงกำหนดให้ใช้ Patient-level Split เท่านั้น เพื่อแยกแยะพยาธิสภาพจากลักษณะเฉพาะตัวบุคคล

Dataset	Source URL	Split Protocol	Patient-level?	Leakage Risk	Recommended for CeXaR?	Notes
NIH ChestX-ray14 (Official)	https://www.emergentmind.com/topics/chestx-ray14-dataset	70/10/20 Image-wise	No	High	No	มี Patient overlap ระหว่าง Train/Val 6,923 ราย
NIH Corrected Split	https://www.medrxiv.org/content/10.1101/2025.10.25.25338784v1.full-text	3-way Split by Patient ID	Yes	Zero	Yes	แก้ปัญหาความปนเปื้อนได้ 100%
CheXpert	https://stanfordmlgroup.github.io/projects/chexnet/	Adjudicated Validation	Yes	Low	Yes	ใช้ Ground Truth จากผู้เชี่ยวชาญ 3-4 ท่าน
MIMIC-CXR	https://physionet.org/content/cxr-lt-iccv-workshop-cvamd/1.0.0/	Long-tailed split	Yes	Low	Yes	แนะนำสำหรับ Pre-training เพื่อเพิ่มความหลากหลาย
Google Expert Split	https://docs.cloud.google.com/healthcare-api/docs/resources/public-datasets/nih-chest	Adjudicated subsets	Yes	Minimal	Yes (Gold Standard)	ชุดข้อมูล 1,962 ภาพที่ผ่านการเอกซเรย์ซ้ำโดยผู้เชี่ยวชาญ

การใช้ Corrected Split เป็นด่านแรกในการป้องกัน Data Leakage ซึ่งจะถูกตรวจสอบอย่างละเอียดในขั้นตอน Audit


--------------------------------------------------------------------------------


3. การตรวจสอบการรั่วไหลของข้อมูล (Leakage Audit)

"Shortcut Learning" คือความเสี่ยงเชิงกลยุทธ์ที่ AI อาจจดจำปัจจัยภายนอก เช่น ยี่ห้อเครื่องสแกน ลายน้ำ หรือโครงสร้างกระดูกของผู้ป่วยแทนการตรวจหารอยโรค

| Leakage Type | How it happens | How to detect | Audit Task | Severity | Evidence URL | | :--- | :--- | :--- | :--- | : :--- | :--- | | Patient Overlap | ผู้ป่วยคนเดิมปรากฏในชุด Train และ Test | AUROC พุ่งสูงผิดปกติ (>0.99) | รันคำสั่ง intersection() ระหว่าง Patient ID lists | Critical | https://pmc.ncbi.nlm.nih.gov/articles/PMC9434540/ | | Global Preprocessing | ใช้สถิติรวมของทั้ง Dataset มา Normalize | ประสิทธิภาพลดลงเมื่อเจอข้อมูลภายนอก (Out-of-distribution) | ตรวจสอบว่า fit() เฉพาะ Train set หรือใช้ Frozen constants | High | https://www.reddit.com/r/MachineLearning/comments/1iu5cgg/r_why_is_there_mixed_views_on_how_traintestval/ | | Metadata Leakage | โมเดลจดจำ Hospital Source หรือประเภทเครื่องสแกน | Gradient focus (Grad-CAM) จับจ้องที่ขอบฟิล์มหรือลายน้ำ | ทดสอบความแม่นยำในการทำนาย Hospital ID/Scanner Type | Medium | https://arxiv.org/pdf/1905.06362 | | Threshold Bias | จูน Youden's J Index บน Test set | F1-score สูงกว่าตอนทำ Validation อย่างมีนัยสำคัญ | ยืนยันว่าค่า Threshold ถูกล็อกก่อนรัน Test inference | High | https://www.mdpi.com/2075-4418/16/8/1227/review_report | | Spatial Erasure | ลด Resolution จนรอยโรคขนาดเล็กหายไป | Performance ในโรค Nodule หรือ Pneumothorax ต่ำผิดปกติ | เปรียบเทียบผลระหว่างโมเดล 224x224 และ 1024x1024 | Medium | https://www.medrxiv.org/content/10.1101/2021.07.30.21261225v1.full-text |

การกำจัด Shortcut เหล่านี้ช่วยให้มั่นใจว่าฉลากข้อมูล (Labels) ที่ใช้เทรนคือเป้าหมายที่โมเดลเรียนรู้จริงๆ


--------------------------------------------------------------------------------


4. การจัดการฉลากข้อมูล (Label Handling)

พยาธิสภาพทรวงอกมักมีความซับซ้อนแบบ Multi-label และมีปัญหา "Label Noise" ประมาณ 10% จากกระบวนการ Text-mining ที่สกัดผลจากรายงานสรุปของแพทย์

Dataset	Label Format	Uncertain Labels?	Recommended Handling	Risk	Audit Task
NIH 14 Labels	Binary Multi-hot	No (Implicit)	"No Finding" = Zero Vector [0,0,...,0]	NLP Error rate ~10%	ตรวจสอบการเรียงลำดับ Canonical Order ลำดับ 1-14
CheXpert	Binary + Uncertain	Yes (U-Labels)	ทดสอบกลยุทธ์ U-Ones และ U-Zeros	อคติจากการตีความ "ไม่แน่ใจ"	เปรียบเทียบ AUROC ระหว่าง U-Ones และ U-Zeros
Class Imbalance	Long-tailed	Yes	ใช้ Loss Function พิเศษ (เช่น Focal ZLPR)	โมเดลมองข้ามโรคหายาก เช่น Hernia (0.2%)	ตรวจสอบค่า PR-AUC ของโรคที่มี Prevalence ต่ำ

คุณภาพของ Label และความละเอียดของภาพ (Resolution) มีความสัมพันธ์กันอย่างยิ่ง โดยเฉพาะในโรคที่ต้องการรายละเอียดสูง


--------------------------------------------------------------------------------


5. ข้อกำหนดการเตรียมข้อมูลภาพ (Preprocessing Requirements)

Image Resolution มีผลโดยตรงต่อ Diagnostic Yield โดยการลดขนาดภาพลงเหลือ 224x224 อาจทำลายรายละเอียดของพยาธิสภาพขนาดเล็ก เช่น Nodule

Baseline	Source URL	Image Size	Normalization	Resize/Crop	Risk if mismatched
CheXNet (DenseNet121)	https://sh-tsang.medium.com/review-chexnet-radiologist-level-pneumonia-detection-on-chest-rays-with-deep-learning-4f85d98e8ef5	224x224	ImageNet Mean/Std	Random Crop / Flip	ขาดรายละเอียดเชิงพื้นที่ (Spatial Details)
MS-CheXNet	https://www.mdpi.com/2227-7390/10/19/3646	Multi-scale	Batch Norm + ReLU	Depthwise Separable (DS-CNN)	โมเดลน้ำหนักเบาแต่อาจหลุดรายละเอียดบางส่วน
Amazon SageMaker	https://aws.amazon.com/blogs/machine-learning/classifying-high-resolution-chest-x-ray-medical-images-with-amazon-sagemaker/	896x896	Weighted Loss	Full Resolution Crop	ค่าใช้จ่ายในการคำนวณเพิ่มขึ้นสูงสุด 81 เท่า
TorchXRayVision	https://www.medrxiv.org/content/10.1101/2025.10.25.25338784v1.full-text	224x224	\mu=121.8, \sigma=57.1	Adaptive Histogram Target	ผลลัพธ์ไม่เสถียรเมื่อใช้ RGB pre-trained

ค่า Input เหล่านี้จะถูกวัดผลด้วย Metrics ที่เหมาะสมเพื่อสะท้อนประสิทธิภาพจริงในสภาวะ Class Imbalance


--------------------------------------------------------------------------------


6. ข้อกำหนดด้านมาตรวัดประสิทธิภาพ (Metric Requirements)

ในชุดข้อมูลที่มี Class Imbalance สูง (Hernia 0.2% ถึง Infiltration 17.8%) ค่า AUROC เพียงอย่างเดียวอาจทำให้เกิดความเข้าใจผิด จึงต้องใช้มาตรวัดที่ครอบคลุมถึง PR-AUC และ Calibration

Metric	How to calculate	Common Mistake	Output File	Evidence URL
AUROC (Per-label)	แยกตามพยาธิสภาพ	รายงานเฉพาะ Macro แล้วมองไม่เห็นจุดบอดบางโรค	per_label_auroc.csv	https://www.mdpi.com/2306-5354/12/6/593
Macro AUROC	ค่าเฉลี่ยไม่ถ่วงน้ำหนัก	การถ่วงน้ำหนัก (Weighted) ทำให้โรคที่พบบ่อยกลบผลโรคหายาก	metrics.json	https://arxiv.org/html/2511.07801v1
PR-AUC	Area under Precision-Recall	ใช้ในสภาวะที่มี True Negatives สูงเกินจริงจน AUROC ดูดีเกินไป	metrics.json	https://www.medrxiv.org/content/10.1101/2025.10.25.25338784v1.full-text
FSS	Harmonic mean ของ Sens/Spec	ปรับ Threshold บนชุด Test ทำให้ค่าสูงผิดปกติ	metrics.json	https://www.medrxiv.org/content/10.1101/2025.10.25.25338784v1.full-text
ECE	Expected Calibration Error	โมเดล Overconfident แต่ทายผิดพลาด	metrics.json	https://glassboxmedicine.com/2019/05/11/automated-chest-x-ray-interpretation/
Youden's J Index	Sens + Spec - 1	ลืมฟิกซ์ค่าจาก Validation set ก่อนรันบนชุด Test	config.yaml	https://www.mdpi.com/2075-4418/16/8/1227/review_report


--------------------------------------------------------------------------------


7. โครงสร้างไฟล์ผลลัพธ์ที่คาดหวัง (Expected Output Files)

เพื่อให้ Codex/Claude และระบบวิศวกรรมสามารถตรวจสอบผลลัพธ์ได้โดยอัตโนมัติ ทุกการทดลองต้องส่งออกไฟล์ตามมาตรฐานนี้:

File	Purpose	Minimum Fields
train_val_test_split.csv	ตรวจสอบ Identity Leakage	Image_ID, Patient_ID, Split_Group
predictions.csv	Logits และ Probabilities สำหรับการตรวจสอบซ้ำ	Image_ID, Logits [1-14], Probabilities [1-14]
metrics.json	สรุปค่า Macro/Micro metrics และ ECE	Macro_AUROC, PR-AUC, ECE, Overall_FSS
per_label_auroc.csv	แจกแจงผลรายโรค (NIH Order)	Disease_Name, AUROC_Value, Sample_Count
config.yaml	บันทึก Hyperparameters และ Constants	Resolution, Normalizer_Mu_Sigma, Tau_Value, Loss_Type

NIH Canonical Order (1-14): Atelectasis, Cardiomegaly, Consolidation, Edema, Effusion, Emphysema, Fibrosis, Hernia, Infiltration, Mass, Nodule, Pleural_Thickening, Pneumonia, Pneumothorax.


--------------------------------------------------------------------------------


8. แผนการตรวจสอบโดย Codex/Claude (Codex/Claude Audit Plan)

ระบบ ต้อง ปฏิบัติตามภารกิจการตรวจสอบคุณภาพ (Quality Assurance) ดังนี้:

Task	Target Files	Expected Result	Pass/Fail Condition
Split Logic Audit	train_val_test_split.csv	set(train).intersection(test) เป็นเซตว่าง	Fail หากพบ Patient ID ซ้ำข้ามชุดข้อมูล
Label Mapping Check	predictions.csv	คอลัมน์ที่ 1-14 ตรงตามลำดับ NIH Canonical Order	Fail หากลำดับไม่ตรงตาม Ground Truth
Leakage Testing	โมเดลสำเร็จรูป	โมเดลต้องไม่สามารถทำนาย Patient ID หรือ Hospital ID ได้	Fail หาก AUROC ในการระบุตัวตนสูงกว่า 0.99
Reproducibility Trace	config.yaml & metrics.json	ค่า Mean/Std ต้องถูกฟิตเฉพาะในชุด Train	Fail หากพบหลักฐานการใช้สถิติจากชุดข้อมูลทั้งหมด


--------------------------------------------------------------------------------


9. โปรโตคอลสรุปที่แนะนำ (Final Recommended Protocol)

ทีมวิศวกรควรดำเนินการตามกลยุทธ์ "Golden Baseline" ต่อไปนี้เพื่อความคุ้มค่าและแม่นยำสูงสุด:

1. Dataset: เริ่มต้นด้วย NIH ChestX-ray14 Corrected Split เพื่อกำจัดปัญหา Identity Leakage 100%
2. Resolution: ใช้ 256x256 เป็นมาตรฐานเริ่มต้น แต่ต้องทำ Benchmark ที่ 1024x1024 สำหรับโรคที่ต้องอาศัยรายละเอียด เช่น Nodule (ระบุพึงระวังว่าการเพิ่มความละเอียดจะเพิ่ม Computational Cost ขึ้น 81 เท่า)
3. Loss Function: ใช้ Focal ZLPR (FZLPR) โดยกำหนดค่า Temperature Parameter \tau = 0.2 ซึ่งให้ค่าเฉลี่ย AUROC สูงสุดที่ 80.45% บน Test set
4. Minimal Metrics: ต้องรายงานผลอย่างน้อย Macro AUROC, PR-AUC, และ ECE ก่อนส่งต่อเข้าสู่กระบวนการ Handoff


--------------------------------------------------------------------------------


10. ข้อความกล่าวอ้างที่ยังไม่ได้รับการยืนยัน (Unverified Claims)

จากการวิเคราะห์ข้อมูล พบประเด็นที่ยังต้องรอการพิสูจน์หรือวิจัยเพิ่มเติม:

Claim	Missing Evidence	What to verify next	Priority
Expert Labels สำหรับ CheXNeXt	ระบุว่าเป็นข้อมูลที่ unreleased และไม่สามารถตรวจสอบได้ในที่สาธารณะ	ตรวจสอบการเข้าถึง Google Cloud Healthcare API สำหรับ adjudicated labels	High
ประสิทธิภาพของ DacNet	ข้อมูลการ Benchmark เทียบกับ MS-CheXNet ยังไม่ชัดเจนใน Source context	ทำการเปรียบเทียบ Computational cost และ Parameter count ของ DacNet	Low
Grad-CAM vs. Grad-ECLIP	ความแตกต่างในการระบุตำแหน่ง (Localization) ของรอยโรคขนาดเล็ก	ทำการประเมิน Intersection over Union (IoU) สำหรับ Visual explanation	Medium

เอกสารฉบับนี้เป็น Engineering Handoff Document ที่กำหนดทิศทางการพัฒนาโมเดล CeXaR ให้มีความถูกต้องตามหลักเกณฑ์วิศวกรรมและจริยธรรมการแพทย์สากล
