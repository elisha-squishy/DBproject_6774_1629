שער

שמות המגישים: אלישע רובין ודניאל סיבוני

שם המערכת: מערכת ניהול דיור מוגן

היחידה הנבחרת: יחידת המגורים והאירועים


תוכן עניינים:
שלב א':
  מבוא

  מבנה בסיס הנתונים
  
  הוספת הנתונים
  
  שלב ב':
  queries

  updates/deletes

  rollback/commit

  alter tables
  
1. מבוא
מערכת זו נועדה לנהל את הפעילות השוטפת של מוסד לדיור מוגן. המערכת שומרת נתונים על חדרים, דיירים, אנשי צוות, אירועים, תפריטים, ציוד ותחזוקה. היא מאפשרת לעקוב אחר פרטי הדיירים, שיבוצם בחדרים, השתתפותם באירועים, וכן אחר בקשות תחזוקה ופריטי מלאי.

הפונקציונליות המרכזית של המערכת כוללת:

ניהול דיירים ושיבוצם לחדרים.

תיעוד אירועים והשתתפות דיירים בהם.

מעקב אחר ציוד ובקשות תחזוקה.

ניהול תפריטי ארוחות והצוות שאחראי לבישול.

זיהוי תפקידים של אנשי צוות במערכת.

מערכת זו נבנתה תוך שימת דגש על שמירת קשרים לוגיים בין הישויות השונות, כדי להבטיח עקביות של הנתונים ויכולת לבצע שאילתות מורכבות בקלות.


2. מבנה בסיס הנתונים
![image](https://github.com/user-attachments/assets/b9e5fdc7-53ca-4a30-9ede-4cc840941214)

![image](https://github.com/user-attachments/assets/6dd9aeaf-ad6b-4419-a97e-b085cca725f0)

2.1 חלוקה ליישויות נפרדות (Normalization)
בחרנו לבנות את המערכת לפי עקרונות נורמליזציה (עד לפחות נורמליזציה מדרגה שלישית), כלומר כל טבלה מייצגת ישות אחת ברורה (למשל: resident, room, event) ואין כפילויות של מידע בין הטבלאות. זה מאפשר:

הפחתת כפילויות ואי עקביות.

עדכון קל ויעיל של נתונים.

מניעת טעויות לוגיות במערכת.

2.2 קשרי 1:רבים ו-n:n
שמנו דגש על יצירת קשרים מדויקים בין הטבלאות:

resident ←→ room:
כל דייר מתגורר בחדר אחד (קשר 1:רבים), ולכן resident כולל מפתח זר ל-room.

resident ←→ event:
מכיוון שדיירים יכולים להשתתף במספר אירועים, וכל אירוע כולל מספר דיירים – יצרנו טבלת קשר visiting_event שתומכת בקשר רבים לרבים (n:n).

maintenance_req:
בקשת תחזוקה היא קשר בין חדר, עובד ופריט. יצרנו טבלה עם מפתח ראשי מורכב הכולל room_id, staff_member_id ו-request_id, על מנת למנוע כפילויות ולזהות חד-ערכית כל בקשה.

is_chef:
כל שף אחראי על ארוחה ביום מסוים – נדרש קשר n:n בין staff_member ל-meal. גם כאן נעשה שימוש במפתח ראשי מורכב: staff_member_id, meal_type, day_of_the_week.

2.3 טבלת meal עם מפתח מורכב
בחרנו שמזהה ייחודי לכל ארוחה יהיה צירוף של meal_type ו-day_of_the_week.
כך ניתן לתאר תפריטים שבועיים חוזרים בצורה פשוטה ללא צורך במספר מזהה רץ.
למשל: (Lunch, Monday) חוזר בכל שבוע.

2.4 שמירה על עקביות עם מפתחות זרים
בכל מקום שבו יש קשר בין טבלאות, שמרנו על מפתחות זרים (FOREIGN KEY) כדי להבטיח שלמות לוגית.
לדוגמה:

לא ניתן להוסיף דייר לחדר שאינו קיים.

בקשת תחזוקה חייבת להתייחס לעובד ולפריט קיימים.

2.5 הפרדת המידע האנושי והלוגיסטי
הפרדנו את המידע על האנשים (דיירים, עובדים) ממידע לוגיסטי (חדרים, ציוד, תפריטים), מה שתורם לארגון ברור של המידע.

2.6 בחירה במזהים מספריים
כל ישות מזוהה בעזרת מזהה מספרי (ID) כמו resident_id, room_id וכו' — זה:

מפשט ביצוע שאילתות.

מאפשר קישורים קלים בין טבלאות.

יעיל מבחינת ביצועים.

3. הוספת הנתונים: הוספנו נתונים ב-3 דרכים: בעזרת בינה מלאכותית, באמצעות סקריפט של פייתון ובעזרת האתר mockaroo
   ![image](https://github.com/user-attachments/assets/b099c012-b736-4788-84e6-43adf4b7452a)

   ![image](https://github.com/user-attachments/assets/3ab5a3f4-7b2b-44ef-bf06-e44adcf852d1)

![image](https://github.com/user-attachments/assets/0b7e1239-6fec-46f8-9af8-abe055ebafe8)

להלן דוג' של גיבוי ושחזור נתונים:
![image](https://github.com/user-attachments/assets/32a5105b-451f-46cd-8568-b104566ac823)
![image](https://github.com/user-attachments/assets/30ef4761-e6c1-48c0-801c-63462844a3f6)







queries:

![image](https://github.com/user-attachments/assets/2f1cecd9-65d4-4165-9fd8-b54f43b03d01)

![image](https://github.com/user-attachments/assets/e6197ff7-67a8-4c01-a8c4-840c1b2ae7fd)

![image](https://github.com/user-attachments/assets/f60e4884-a325-4834-95d8-edbeb1a5bd25)

![image](https://github.com/user-attachments/assets/87ccc2a3-b0e2-4e00-a19c-0756caa2c6d9)

![image](https://github.com/user-attachments/assets/2c24c86b-f5e0-4332-a85c-f9034b6ef3bb)

![image](https://github.com/user-attachments/assets/960c5183-ed41-4bc1-9c62-6e58971ed460)

![image](https://github.com/user-attachments/assets/e9d11784-7e2b-44a0-8913-8467e15ad53d)

![image](https://github.com/user-attachments/assets/3cccd008-8325-4548-a91a-b61b9f1938c9)


updates/deletes:

![image](https://github.com/user-attachments/assets/6fb9a8a7-711e-4ff7-a153-19e2e4213b86)

![image](https://github.com/user-attachments/assets/de5fe9d8-a3ef-4bb4-b0b1-7beff2ff7cdf)

![image](https://github.com/user-attachments/assets/74358ec0-2c09-4503-8f8c-43de362089de)

![image](https://github.com/user-attachments/assets/6ec0a6e3-f280-4046-953b-0b196217be26)

![image](https://github.com/user-attachments/assets/501cc685-139e-4c8c-ae83-0927765fb4f8)

![image](https://github.com/user-attachments/assets/78dbb661-c8ee-4792-ab37-8e53eb2b704c)

![image](https://github.com/user-attachments/assets/0ee00672-8a99-4bd6-824e-9f6ede041d67)

![image](https://github.com/user-attachments/assets/c707d835-7368-42a7-b796-f9f2d990b8d4)

![image](https://github.com/user-attachments/assets/8a5fe543-f0f8-4ed0-b6f0-7aab2c303ed1)



![image](https://github.com/user-attachments/assets/77b7c447-64b6-4713-a017-a9b7e99f97c1)

![image](https://github.com/user-attachments/assets/2ecc9819-dbaf-4efc-9381-1ccaa0ecfcbe)

![image](https://github.com/user-attachments/assets/53169bd6-9408-468b-b43f-89be5e712b9a)

![image](https://github.com/user-attachments/assets/f1349043-9726-4605-b98b-03aeaf54c566)

![image](https://github.com/user-attachments/assets/bfdc6a84-b721-43cd-a5bd-282f70748004)

![image](https://github.com/user-attachments/assets/9bd89cd1-04c5-4f9a-8652-61a56b635ac8)

![image](https://github.com/user-attachments/assets/280f449a-531a-412d-a4bb-2f283d84bac5)

![image](https://github.com/user-attachments/assets/cfe2454e-858d-4916-a34c-6c86efe66c64)

![image](https://github.com/user-attachments/assets/2d858dcf-cdef-4239-861c-ea4adfdda494)


rollback/commit:

![image](https://github.com/user-attachments/assets/d658916b-1a70-4cea-8078-7832fd439179)

![image](https://github.com/user-attachments/assets/2e6e8ad1-979f-4bc4-a80e-121ddf07d6f8)

![image](https://github.com/user-attachments/assets/3a36fbcb-4fd8-4e01-9d47-9340ece0eacd)

![image](https://github.com/user-attachments/assets/0a68e355-fa14-48eb-bd15-2e99663dccbe)


![image](https://github.com/user-attachments/assets/c6e5e853-f4ea-4e13-aad5-a3c835d7dbbe)

![image](https://github.com/user-attachments/assets/6c7ed2da-bb00-42a4-9f56-9265c1c55d8e)

![image](https://github.com/user-attachments/assets/86cb830e-4d8b-4170-bd22-a1e71e50337e)

![image](https://github.com/user-attachments/assets/8e5254a7-86bb-4683-9d91-a05118e85831)


alter tables:

![image](https://github.com/user-attachments/assets/231579c8-bdc8-42b8-bb6d-381a050cdad6)

![image](https://github.com/user-attachments/assets/951d81eb-6a84-466d-b558-58385699c864)

![image](https://github.com/user-attachments/assets/cfb18ccd-5bb8-4cab-9b30-1534584179f5)

![image](https://github.com/user-attachments/assets/2c54d59c-b783-4fd3-963f-ff6475dd0b1a)

![image](https://github.com/user-attachments/assets/d4aaf688-fe0c-4227-9a18-b5b2bd6e721b)

![image](https://github.com/user-attachments/assets/306578ff-7fe8-4d1d-9b04-aa294176ee97)

![image](https://github.com/user-attachments/assets/9cf15d1d-56c4-4ba6-a1bf-27a7825d4271)


