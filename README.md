# מערכת ניהול דיור מוגן

**שמות המגישים:** אלישע רובין ודניאל סיבוני  
**שם המערכת:** מערכת ניהול דיור מוגן  
**היחידה הנבחרת:** יחידת המגורים והאירועים

---

## תוכן עניינים

- [1. מבוא](#1-מבוא)
- [2. מבנה בסיס הנתונים](#2-מבנה-בסיס-הנתונים)
  - [2.1 חלוקה ליישויות נפרדות (Normalization)](#21-חלוקה-ליישויות-נפרדות-normalization)
  - [2.2 קשרי 1:רבים ו-n:n](#22-קשרי-1רבים-ו-nn)
  - [2.3 טבלת meal עם מפתח מורכב](#23-טבלת-meal-עם-מפתח-מורכב)
  - [2.4 שמירה על עקביות עם מפתחות זרים](#24-שמירה-על-עקביות-עם-מפתחות-זרים)
  - [2.5 הפרדת המידע האנושי והלוגיסטי](#25-הפרדת-המידע-האנושי-והלוגיסטי)
  - [2.6 בחירה במזהים מספריים](#26-בחירה-במזהים-מספריים)
- [3. הוספת הנתונים](#3-הוספת-הנתונים)
- [4. שלב ב'](#4-שלב-ב)
  - [4.1 Queries](#41-queries)
  - [4.2 Updates/Deletes](#42-updatesdeletes)
  - [4.3 Rollback/Commit](#43-rollbackcommit)
  - [4.4 Alter Tables](#44-alter-tables)
- [5. שלב ג'- merge עם מבנה נתונים אחר](#5-שלב-ג)
---

## 1. מבוא

מערכת זו נועדה לנהל את הפעילות השוטפת של מוסד לדיור מוגן. המערכת שומרת נתונים על חדרים, דיירים, אנשי צוות, אירועים, תפריטים, ציוד ותחזוקה.  
היא מאפשרת לעקוב אחר:

- ניהול דיירים ושיבוצם לחדרים  
- תיעוד אירועים והשתתפות דיירים  
- מעקב אחר ציוד ובקשות תחזוקה  
- ניהול תפריטי ארוחות והצוות שאחראי לבישול  
- זיהוי תפקידים של אנשי צוות במערכת  

---

## 2. מבנה בסיס הנתונים

![DB Diagram 1](https://github.com/user-attachments/assets/b9e5fdc7-53ca-4a30-9ede-4cc840941214)  
![DB Diagram 2](https://github.com/user-attachments/assets/6dd9aeaf-ad6b-4419-a97e-b085cca725f0)

### 2.1 חלוקה ליישויות נפרדות (Normalization)

בחרנו לעבוד לפי עקרונות הנורמליזציה (עד דרגה 3) כדי להבטיח:

- הפחתת כפילויות
- עדכון יעיל
- מניעת שגיאות לוגיות

### 2.2 קשרי 1:רבים ו-n:n

- `resident` ←→ `room` – קשר 1:רבים  
- `resident` ←→ `event` – טבלת קשר `visiting_event` לקשר n:n  
- `maintenance_req` – מפתח ראשי מורכב: `room_id`, `staff_member_id`, `request_id`  
- `is_chef` – קשר n:n בין `staff_member` ל-`meal`

### 2.3 טבלת meal עם מפתח מורכב

צירוף `meal_type + day_of_the_week` מהווה מזהה ייחודי.

### 2.4 שמירה על עקביות עם מפתחות זרים

- לא ניתן להוסיף דייר לחדר לא קיים  
- בקשת תחזוקה חייבת להתייחס לישות קיימת

### 2.5 הפרדת המידע האנושי והלוגיסטי

מפריד בין:

- ישויות אנושיות (דיירים, עובדים)  
- ישויות לוגיסטיות (חדרים, ציוד)

### 2.6 בחירה במזהים מספריים

למשל `resident_id`, `room_id`:

- מפשט שאילתות  
- קישורים פשוטים  
- יעילות בביצועים

---

## 3. הוספת הנתונים

הוספנו נתונים ב-3 דרכים:
1. בינה מלאכותית  
2. סקריפט Python  
3. אתר [Mockaroo](https://mockaroo.com)

![image](https://github.com/user-attachments/assets/b099c012-b736-4788-84e6-43adf4b7452a)  
![image](https://github.com/user-attachments/assets/3ab5a3f4-7b2b-44ef-bf06-e44adcf852d1)  
![image](https://github.com/user-attachments/assets/0b7e1239-6fec-46f8-9af8-abe055ebafe8)

**דוגמה לגיבוי ושחזור נתונים:**  
![image](https://github.com/user-attachments/assets/32a5105b-451f-46cd-8568-b104566ac823)  
![image](https://github.com/user-attachments/assets/30ef4761-e6c1-48c0-801c-63462844a3f6)

---

## 4. שלב ב'

### 4.1 Queries

- **אירועים שבהם דייר השתתף**  
  ![image](https://github.com/user-attachments/assets/2f1cecd9-65d4-4165-9fd8-b54f43b03d01)

- **בקשות תחזוקה לפי חדר וקיבולת**  
  ![image](https://github.com/user-attachments/assets/e6197ff7-67a8-4c01-a8c4-840c1b2ae7fd)

- **התפלגות השתתפות באירועים**  
  ![image](https://github.com/user-attachments/assets/f60e4884-a325-4834-95d8-edbeb1a5bd25)

- **כמה בקשות סיים כל איש צוות**  
  ![image](https://github.com/user-attachments/assets/87ccc2a3-b0e2-4e00-a19c-0756caa2c6d9)

- **חדרים עם פחות/יותר מ-2 בקשות תחזוקה**  
  ![image](https://github.com/user-attachments/assets/2c24c86b-f5e0-4332-a85c-f9034b6ef3bb)

- **מספר שפים פעילים לאורך זמן**  
  ![image](https://github.com/user-attachments/assets/960c5183-ed41-4bc1-9c62-6e58971ed460)

- **השוואת תפקידים מול ביצועים**  
  ![image](https://github.com/user-attachments/assets/e9d11784-7e2b-44a0-8913-8467e15ad53d)

- **קיבולת מול תפוסה בחדרים**  
  ![image](https://github.com/user-attachments/assets/3cccd008-8325-4548-a91a-b61b9f1938c9)

### 4.2 Updates/Deletes

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

### 4.3 Rollback/Commit

![image](https://github.com/user-attachments/assets/d658916b-1a70-4cea-8078-7832fd439179)

![image](https://github.com/user-attachments/assets/2e6e8ad1-979f-4bc4-a80e-121ddf07d6f8)

![image](https://github.com/user-attachments/assets/3a36fbcb-4fd8-4e01-9d47-9340ece0eacd)

![image](https://github.com/user-attachments/assets/0a68e355-fa14-48eb-bd15-2e99663dccbe)


![image](https://github.com/user-attachments/assets/c6e5e853-f4ea-4e13-aad5-a3c835d7dbbe)

![image](https://github.com/user-attachments/assets/6c7ed2da-bb00-42a4-9f56-9265c1c55d8e)

![image](https://github.com/user-attachments/assets/86cb830e-4d8b-4170-bd22-a1e71e50337e)

![image](https://github.com/user-attachments/assets/8e5254a7-86bb-4683-9d91-a05118e85831)


### 4.4 alter tables:

![image](https://github.com/user-attachments/assets/231579c8-bdc8-42b8-bb6d-381a050cdad6)

![image](https://github.com/user-attachments/assets/951d81eb-6a84-466d-b558-58385699c864)

![image](https://github.com/user-attachments/assets/cfb18ccd-5bb8-4cab-9b30-1534584179f5)

![image](https://github.com/user-attachments/assets/2c54d59c-b783-4fd3-963f-ff6475dd0b1a)

![image](https://github.com/user-attachments/assets/d4aaf688-fe0c-4227-9a18-b5b2bd6e721b)

![image](https://github.com/user-attachments/assets/306578ff-7fe8-4d1d-9b04-aa294176ee97)

![image](https://github.com/user-attachments/assets/9cf15d1d-56c4-4ba6-a1bf-27a7825d4271)

## 5. שלב ג
ביצענו merge עם בסיס נתונים אחר שאחראי על הדיירים. זה הERD של בסיס הנתונים:
![other DB ERD](https://github.com/user-attachments/assets/7fa468b5-5d96-467e-8dd7-4eb54bef3dec)
וזה ה DSD:
![other DB DSD](https://github.com/user-attachments/assets/91917173-b48e-4270-b905-3d9ae675d12c)

והנה אותם תרשימים אחרי ה merge:
![updated ERD](https://github.com/user-attachments/assets/d7d46920-f0f7-4da7-b80e-cb892966f7e5)
![updated DSD](https://github.com/user-attachments/assets/302ee72e-4fd3-4532-a9d1-d5e9b85eda03)

החלטנו לבצע את האינטגרציה כך שכאשר היתה טבלה משותפת (לדוג' לשנינו היה טבלה של  resident אז השתמשנו בטבלה שלהם בסוף). הדבר לא יצר בעיות התאמה בגלל ששנינו הגדרנו את המפתחות של רוב הדברים פשוט במספרים בין 1 ל-1000.
עדיין נתקלנו בבעיות מפני שטבלאת resident שלבם כללה פחות אנשים מטבלאת resident שלנו מה שגרם לבעיות בטבלאות אחרות שלנו שנשענו על resident, אז ביצענו merge Into בין הטבלאות:
<pre>
```
MERGE INTO resident AS t1
USING resident_temp AS t2  -- our table
ON t1.residentid = t2.resident_id
WHEN NOT MATCHED THEN
    INSERT (residentid, firstname, lastname, dateofbirth, admissiondate, roomid)
    VALUES (
        t2.resident_id,
        SPLIT_PART(t2.resident_name, ' ', 1),
        SPLIT_PART(t2.resident_name, ' ', 2),
        t2.resident_dob,
        '01/01/2021',
        t2.room_id
    );
</pre>
 דהיינו הוספנו לטבלה שלהם את כל האיברים בטבלה שלנו שלא קיימים בטבלה שלהם.
 חוץ מזה, האינטגרציה רצה על מי מנוחות.
 ### יצירת המבטים
 החלטנו ליצור שני מבטים. המבט הראשון הוא עבור עובדי התחזוקה ונותן להם את המידע המעניין אותם, קרי: משימות שהם צריכים לעשות, החדרים שצריכים טיפול וכו'. הנה איך הוא נראה:
![image](https://github.com/user-attachments/assets/5b1ef492-1970-4d08-b31b-250c8bf1e101)
 
הרצנו שני שאילתות עליו. הראשונה נועדה לברר אילו מוצרים זקוקים אליהם בשביל משימות שעומדות להתקיים שיש מחסור מהם:
![image](https://github.com/user-attachments/assets/c367aa38-4a79-4ae1-ac57-0868945a65af)
השאילתא השנייה מחפשת את כל המשימות שעובד מסויים צריך לבצע, יחד עם מספר החדר בו המשימה מתבצעת.

![image](https://github.com/user-attachments/assets/d8330e17-cf4c-4163-a933-26b60fbd7825)
המבט השני הוא מידע בשביל המשפחה, דהיינו: הסטוריית ביקורים, ההיסטוריה הרפואית של הדייר ומידע על הרופאים שלו וכו'.
![image](https://github.com/user-attachments/assets/334323e7-49e5-412f-aa1a-c79da62bc121)

הרצנו עליו שני שאילתות. הראשונה מחפשת מידע על כל הרופאים שטיפלו בחולה מסויים:
![image](https://github.com/user-attachments/assets/78436173-862d-4e55-8549-e87df9710051)

השנייה מיצרת את הסטוריית הטיפולים של חולה מסויים:

![image](https://github.com/user-attachments/assets/0358bcd8-a9aa-490a-b054-a8978c837eca)





