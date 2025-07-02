# מערכת ניהול דיור מוגן

**שמות המגישים:** אלישע רובין ודניאל סיבוני  
**שם המערכת:** מערכת ניהול דיור מוגן  
**היחידה הנבחרת:** יחידת המגורים והאירועים

---

## תוכן עניינים

- [מבוא](#-מבוא)
- [1. שלב א' - מבנה בסיס הנתונים](#1-מבנה-בסיס-הנתונים)
  - [1.1 חלוקה ליישויות נפרדות (Normalization)](#11-חלוקה-ליישויות-נפרדות-normalization)
  - [1.2 קשרי 1:רבים ו-n:n](#12-קשרי-1רבים-ו-nn)
  - [1.3 טבלת meal עם מפתח מורכב](#13-טבלת-meal-עם-מפתח-מורכב)
  - [1.4 שמירה על עקביות עם מפתחות זרים](#14-שמירה-על-עקביות-עם-מפתחות-זרים)
  - [1.5 הפרדת המידע האנושי והלוגיסטי](#15-הפרדת-המידע-האנושי-והלוגיסטי)
  - [1.6 בחירה במזהים מספריים](#16-בחירה-במזהים-מספריים)
  - [1.7 הוספת הנתונים](#17-הוספת-הנתונים)
- [2. שלב ב'](#2-שלב-ב)
  - [2.1 Queries](#21-queries)
  - [2.2 Updates/Deletes](#22-updatesdeletes)
  - [2.3 Rollback/Commit](#23-rollbackcommit)
  - [2.4 Alter Tables](#24-alter-tables)
- [3. שלב ג'- merge עם מבנה נתונים אחר](#3-שלב-ג)

- [4. שלב ד' - pg/plsql](#4-שלב-ד)
- [5. שלב ה' - GUI](#5-שלב-ה)
---

## מבוא

מערכת זו נועדה לנהל את הפעילות השוטפת של מוסד לדיור מוגן. המערכת שומרת נתונים על חדרים, דיירים, אנשי צוות, אירועים, תפריטים, ציוד ותחזוקה.  
היא מאפשרת לעקוב אחר:

- ניהול דיירים ושיבוצם לחדרים  
- תיעוד אירועים והשתתפות דיירים  
- מעקב אחר ציוד ובקשות תחזוקה  
- ניהול תפריטי ארוחות והצוות שאחראי לבישול  
- זיהוי תפקידים של אנשי צוות במערכת  

---

## 1. מבנה בסיס הנתונים

![DB Diagram 1](https://github.com/user-attachments/assets/b9e5fdc7-53ca-4a30-9ede-4cc840941214)  
![DB Diagram 2](https://github.com/user-attachments/assets/6dd9aeaf-ad6b-4419-a97e-b085cca725f0)

### 1.1 חלוקה ליישויות נפרדות (Normalization)

בחרנו לעבוד לפי עקרונות הנורמליזציה (עד דרגה 3) כדי להבטיח:

- הפחתת כפילויות
- עדכון יעיל
- מניעת שגיאות לוגיות

### 1.2 קשרי 1:רבים ו-n:n

- `resident` ←→ `room` – קשר 1:רבים  
- `resident` ←→ `event` – טבלת קשר `visiting_event` לקשר n:n  
- `maintenance_req` – מפתח ראשי מורכב: `room_id`, `staff_member_id`, `request_id`  
- `is_chef` – קשר n:n בין `staff_member` ל-`meal`

### 1.3 טבלת meal עם מפתח מורכב

צירוף `meal_type + day_of_the_week` מהווה מזהה ייחודי.

### 1.4 שמירה על עקביות עם מפתחות זרים

- לא ניתן להוסיף דייר לחדר לא קיים  
- בקשת תחזוקה חייבת להתייחס לישות קיימת

### 1.5 הפרדת המידע האנושי והלוגיסטי

מפריד בין:

- ישויות אנושיות (דיירים, עובדים)  
- ישויות לוגיסטיות (חדרים, ציוד)

### 1.6 בחירה במזהים מספריים

למשל `resident_id`, `room_id`:

- מפשט שאילתות  
- קישורים פשוטים  
- יעילות בביצועים

---

## 1.7 הוספת הנתונים

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

## 2. שלב ב'

### 2.1 Queries

- **5 האירועים הכי פופולריים**
- 
  
- ![image](https://github.com/user-attachments/assets/b260cea6-7fee-4682-8e14-fd5ee47bc3d7)
- 


- **בקשות תחזוקה לפי חדר וקיבולת החדר**
- 
  ![image](https://github.com/user-attachments/assets/e6197ff7-67a8-4c01-a8c4-840c1b2ae7fd)
  

- **התפלגות השתתפות באירועים**
-  
  ![image](https://github.com/user-attachments/assets/f60e4884-a325-4834-95d8-edbeb1a5bd25)
  

- **3 הפריטים שהשתמשו בהם הכי הרבה בבבקשות תחזוקה**
- 
  ![image](https://github.com/user-attachments/assets/912d2c1a-e455-4185-8a06-d423266fdfc4)
  


- **חדרים עם פחות/יותר מ-2 בקשות תחזוקה**
- 
  ![image](https://github.com/user-attachments/assets/2c24c86b-f5e0-4332-a85c-f9034b6ef3bb)
  

- **מספר השפים שמכינים ארוחות לאורך הזמן**
- 
  ![image](https://github.com/user-attachments/assets/960c5183-ed41-4bc1-9c62-6e58971ed460)
  

- **מציאת העובדים שסיימו הכי הרבה משימות מכל תפקיד**
- 
  ![image](https://github.com/user-attachments/assets/e9d11784-7e2b-44a0-8913-8467e15ad53d)
  

- **אחוזי התפוסה בפועל של החדרים לעומת הקיבולת המקסימלית בבניין**
- 
  ![image](https://github.com/user-attachments/assets/e99bf87e-34ba-499b-a023-efc4fa442e6e)
  


### 2.2 Updates/Deletes

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

### 2.3 Rollback/Commit

![image](https://github.com/user-attachments/assets/d658916b-1a70-4cea-8078-7832fd439179)

![image](https://github.com/user-attachments/assets/2e6e8ad1-979f-4bc4-a80e-121ddf07d6f8)

![image](https://github.com/user-attachments/assets/3a36fbcb-4fd8-4e01-9d47-9340ece0eacd)

![image](https://github.com/user-attachments/assets/0a68e355-fa14-48eb-bd15-2e99663dccbe)


![image](https://github.com/user-attachments/assets/c6e5e853-f4ea-4e13-aad5-a3c835d7dbbe)

![image](https://github.com/user-attachments/assets/6c7ed2da-bb00-42a4-9f56-9265c1c55d8e)

![image](https://github.com/user-attachments/assets/86cb830e-4d8b-4170-bd22-a1e71e50337e)

![image](https://github.com/user-attachments/assets/8e5254a7-86bb-4683-9d91-a05118e85831)


### 2.4 alter tables:

![image](https://github.com/user-attachments/assets/231579c8-bdc8-42b8-bb6d-381a050cdad6)

![image](https://github.com/user-attachments/assets/951d81eb-6a84-466d-b558-58385699c864)

![image](https://github.com/user-attachments/assets/cfb18ccd-5bb8-4cab-9b30-1534584179f5)

![image](https://github.com/user-attachments/assets/2c54d59c-b783-4fd3-963f-ff6475dd0b1a)

![image](https://github.com/user-attachments/assets/d4aaf688-fe0c-4227-9a18-b5b2bd6e721b)

![image](https://github.com/user-attachments/assets/306578ff-7fe8-4d1d-9b04-aa294176ee97)

![image](https://github.com/user-attachments/assets/9cf15d1d-56c4-4ba6-a1bf-27a7825d4271)

## 3. שלב ג
ביצענו merge עם בסיס נתונים אחר שאחראי על הדיירים. זה הERD של בסיס הנתונים:
![other DB ERD](https://github.com/user-attachments/assets/7fa468b5-5d96-467e-8dd7-4eb54bef3dec)
וזה ה DSD:
![other DB DSD](https://github.com/user-attachments/assets/91917173-b48e-4270-b905-3d9ae675d12c)

והנה אותם תרשימים אחרי ה merge:
![updated ERD](https://github.com/user-attachments/assets/d7d46920-f0f7-4da7-b80e-cb892966f7e5)
![updated DSD](https://github.com/user-attachments/assets/302ee72e-4fd3-4532-a9d1-d5e9b85eda03)

החלטנו לבצע את האינטגרציה כך שכאשר היתה טבלה משותפת (לדוג' לשנינו היה טבלה של  resident אז השתמשנו בטבלה שלהם בסוף).
הדבר לא יצר בעיות התאמה בגלל ששנינו הגדרנו את המפתחות של רוב הדברים פשוט במספרים בין 1 ל-1000.
עדיין נתקלנו בבעיות מפני שטבלאת resident שלבם כללה פחות אנשים מטבלאת resident שלנו מה שגרם לבעיות בטבלאות אחרות שלנו שנשענו על resident, אז ביצענו merge Into בין הטבלאות:
<pre>
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
 החלטנו ליצור שני מבטים. המבט הראשון הוא עבור עובדי התחזוקה ונותן להם את המידע המעניין אותם, קרי: משימות שהם צריכים לעשות, החדרים שצריכים טיפול וכו'. הנה איך היצירה שלו נראית ואיך הוא נראה:
 <pre>
create view caregiver_maintenance as 
select c.caregiverid, (c.firstname || ' ' || c.lastname) caregiver_name, i.item_name, i.quantity, r.roomnumber, mr.req_description, mr.req_status
from maintenance_req mr
join caregiver c on mr.staff_member_id = c.caregiverid
join inventory i on mr.item_id = i.item_id
join department d on c.departmentid = d.departmentid
join room r on mr.room_id = r.roomid
where d.name not ilike '%Care%' and d.name not ilike '%nursing%'
 </pre>
 
![image](https://github.com/user-attachments/assets/5b1ef492-1970-4d08-b31b-250c8bf1e101)
 
הרצנו שני שאילתות עליו. הראשונה נועדה לברר אילו מוצרים זקוקים אליהם בשביל משימות שעומדות להתקיים שיש מחסור מהם:

![image](https://github.com/user-attachments/assets/c367aa38-4a79-4ae1-ac57-0868945a65af)

השאילתא השנייה מחפשת את כל המשימות שעובד מסויים צריך לבצע, יחד עם מספר החדר בו המשימה מתבצעת.

![image](https://github.com/user-attachments/assets/22d71c33-c191-4297-99fe-e748e95ecca5)


המבט השני הוא מידע בשביל המשפחה, דהיינו: הסטוריית ביקורים, ההיסטוריה הרפואית של הדייר ומידע על הרופאים שלו וכו'.
<pre>
create view family_view as 
select fv.visitdate, fv.visitorname, r.firstname || ' ' || r.lastname resident_name,
c.firstname || ' ' || c.lastname caregiver_name, c.phone caregiver_phone, mt.treatmentdate, mt.treatmenttype
from familyvisit fv
join medicaltreatment mt on mt.residentid = fv.residentid
join caregiver c on c.caregiverid = mt.caregiverid
join resident r on r.residentid = mt.residentid
</pre>

![image](https://github.com/user-attachments/assets/334323e7-49e5-412f-aa1a-c79da62bc121)


הרצנו עליו שני שאילתות. הראשונה מחפשת מידע על כל הרופאים שטיפלו בחולה מסויים:
![image](https://github.com/user-attachments/assets/78436173-862d-4e55-8549-e87df9710051)

השנייה מיצרת את הסטוריית הטיפולים של חולה מסויים:

![image](https://github.com/user-attachments/assets/0358bcd8-a9aa-490a-b054-a8978c837eca)




## 4. שלב ד
יצרנו 3 פונקציונאליות חדשות באמצעות pg/plsql- פונקציה לעידכון בטבלאת האירועים על ימי הולדת של דיירים, פונקציה להמלצה על אירועים לדייר כלשהו על פי כמה משתתפים אחרים הולכים לאותו אירוע, ומערכת להורדת כמות המוצרים במערכת בצורה בטוחה.

בנוסף לכך, יצרנו טבלאות חדשות ל updates_log, orders כדי לתאר את העידכונים וכדי לערוך הזמנות מוצרים בהתאמה

### 4.1 עידכון ימי הולדת
יצרנו פונקציה שעוברת על כל הדיירים, ואם היומולדת שלהם מחר אז יוצרים איבנט חדש בטבלה event. 

יצרנו עבור זה גם פונקציות עזר כגון get_resident_age ו add_event שדואג להכנסת אירוע בלי צורך להגדיר מפתח יחודי

```sql
-- update birthdays, make the location of the event at the resident's room and record in log
CREATE OR REPLACE FUNCTION create_upcoming_birthday_events()
RETURNS VOID AS $$
DECLARE
  r RECORD;
  v_event_date DATE := CURRENT_DATE + INTERVAL '1 day';
  v_age INT;
  v_room INT;
  v_event_name VARCHAR(100);
BEGIN
  FOR r IN
    SELECT residentid, firstname, lastname, dateofbirth, roomnumber
    FROM resident re
    JOIN room ro ON re.roomid = ro.roomid 
    WHERE EXTRACT(MONTH FROM re.dateofbirth) = EXTRACT(MONTH FROM v_event_date)
      AND EXTRACT(DAY FROM re.dateofbirth) = EXTRACT(DAY FROM v_event_date)
  LOOP
    -- Use existing function to get current age
    v_age := get_resident_age(r.residentid) + 1;
    v_room := r.roomnumber;

    -- Construct event title
    v_event_name := r.firstname || ' ' || r.lastname || '''s ' || v_age || ' birthday!';

    -- Insert birthday event
    CALL add_event(v_event_name, v_event_date, CAST(v_room AS VARCHAR));

    -- Log the event creation
    INSERT INTO updates_log(description)
    VALUES ('Birthday event added: "' || v_event_name || '" for ' || v_event_date);
  END LOOP;
END;
$$ LANGUAGE plpgsql;

-- select create_upcoming_birthday_events();
```
ולהלן התוצאה:


![image](https://github.com/user-attachments/assets/cda65f7b-83f7-4d43-85cb-a30d063ecfd9)


![image](https://github.com/user-attachments/assets/1fbbc458-75d0-4ae1-b04e-a0e1cedc2be7)



### 4.2 המלצת אירועים
יצרנו מערכת המלצת אירועים שממליצה עבור דייר מסוים אירועים שאנשים בטווח גילאים שלו ומאותו מין כמוהו הולכים אליהם גם
להלן הקוד:
```sql
-- Main function - recommend events based on similar age groups
CREATE OR REPLACE FUNCTION recommend_events(target_resident_id INT)
RETURNS TABLE(
    event_date DATE,
    event_location VARCHAR,
    similar_age_attendees BIGINT
)
LANGUAGE plpgsql
AS $$
DECLARE
    target_age INT;
BEGIN
    -- Log the request
    CALL log_recommendation_request(target_resident_id);
    
    -- Get target resident's age
    SELECT get_resident_age(target_resident_id) INTO target_age;
    
    -- Return future events attended by residents within 5 years of target's age
    RETURN QUERY
    SELECT 
        e.event_date,
        e.event_location,
        COUNT(ve.resident_id) as similar_age_attendees
    FROM event e
    JOIN visiting_event ve ON e.event_id = ve.event_id
    -- WHERE e.event_date >= CURRENT_DATE
      WHERE e.event_id NOT IN (
          SELECT event_id 
          FROM visiting_event 
          WHERE resident_id = target_resident_id
      )
      AND get_resident_age(ve.resident_id) BETWEEN (target_age - 5) AND (target_age + 5)
    GROUP BY e.event_id, e.event_date, e.event_location
    ORDER BY COUNT(ve.resident_id) DESC
    LIMIT 10;
END;
$$;

-- SELECT * FROM recommend_events(123);
```
ולהלן התוצאה:


![image](https://github.com/user-attachments/assets/090cd5ef-ffd0-40f1-8e9e-f49ad9b6dc7f)



### 4.3 עידכון מלאי
יצרנו פרוצדורה שמקטינה את הכמות של מוצר כלשהו במלאי, ומוודאת שלא מקטינים אותה ביותר מידי. בנוסף לכך, יצרנו טריגר שמכניס בצורה אוטומטית לטבלה orders הזמנה של מוצר אם הכמות שלו במלאי קטנה מחמש

להלן הקוד:
```sql
CREATE OR REPLACE PROCEDURE decrease_item_quantity(
    target_item_id INT,
    decrease_amount INT DEFAULT 1
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Update the quantity
	
    UPDATE inventory 
    SET quantity = quantity - decrease_amount
    WHERE item_id = target_item_id AND quantity > decrease_amount;
	
    -- Check if update affected any rows
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Item with ID % not found', target_item_id;
    END IF;
    
    INSERT INTO updates_log(description)
	VALUES('Decreased quantity of item ' || target_item_id || ' by ' || decrease_amount);
END;
$$;
```
להלן הקוד עבור הטריגר (יצרנו פונקציית עזר שפרקטית מכניסה את ההזמנה לטבלה)
```sql
CREATE OR REPLACE TRIGGER order_low_stock
    AFTER UPDATE OF quantity ON inventory
    FOR EACH ROW
    WHEN (NEW.quantity < 5)
    EXECUTE FUNCTION auto_order_low_stock();


CREATE OR REPLACE FUNCTION auto_order_low_stock()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Check if quantity dropped below 5
    IF NEW.quantity < 5 THEN
        -- Check if we haven't already placed a pending order for this item
        IF NOT EXISTS (
            SELECT 1 FROM orders 
            WHERE item_id = NEW.item_id 
            AND status = 'PENDING'
        ) THEN
            -- Insert new order
            INSERT INTO orders (item_id, item_name, order_quantity)
            VALUES (NEW.item_id, NEW.item_name, 10);
            
            RAISE NOTICE 'Auto-ordered 10 units of % (ID: %) - stock level: %', 
                         NEW.item_name, NEW.item_id, NEW.quantity;
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$;
```

ולהלן התוצאה:


![image](https://github.com/user-attachments/assets/d426bf15-3bb8-45e1-a43f-cca006c36360)


![image](https://github.com/user-attachments/assets/4333b0a1-6365-494f-8d1d-010bc59185b5)



### 4.4 פונקציות נוספות
יצרנו טריגר שמוודא שלא מכניסים לתוך meintenance req בקשה שהיא לא recived.
```sql
CREATE OR REPLACE FUNCTION public.check_maintenance_status()
RETURNS trigger
BEGIN
	IF UPPER(NEW.req_status) <> 'RECEIVED' THEN
    RAISE EXCEPTION 'Maintenance request status must be "Received".';
END IF;
RETURN NEW;
END;
```
### 4.5 פונקציות עזר
יצרנו פונקציה שמטרתה היא שנוכל להכניס אירוע ושהיא תחולל לנו מפתח ייחודי לאירוע:
```sql
--generates a unique id for an event i want to insert
CREATE OR REPLACE PROCEDURE add_event(
  p_name VARCHAR(100),
  p_date DATE,
  p_location VARCHAR(100)
)
LANGUAGE plpgsql
AS $$
DECLARE
  v_event_id INT;
BEGIN
  -- Generate unique event_id using timestamp and random number
  v_event_id := TRUNC(RANDOM() * 100000)::INT;

  -- Insert into event table
  INSERT INTO event(event_id, event_name, event_date, event_location)
  VALUES (v_event_id, p_name, p_date, p_location);

  -- Optional: output confirmation
  RAISE NOTICE 'Event % added with ID: %', p_name, v_event_id;
END;
$$;
```

בנוסף לכך יצרנו פונקיית עזר שמחשבת לנו את גילו של דייר כלשהו

```sql
-- helper function to calculate a resident age
CREATE OR REPLACE FUNCTION get_resident_age(p_resident_id INT)
RETURNS INT AS $$
DECLARE
  v_dob DATE;
  v_age INT;
BEGIN
  -- Get the resident's date of birth
  SELECT dateofbirth INTO v_dob
  FROM resident
  WHERE resident_id = p_resident_id;

  -- Calculate the age
  v_age := DATE_PART('year', AGE(CURRENT_DATE, v_dob));

  RETURN v_age;

EXCEPTION
  WHEN NO_DATA_FOUND THEN
    RAISE EXCEPTION 'Resident with ID % not found.', p_resident_id;
END;
$$ LANGUAGE plpgsql;
```

## 5. שלב ה
בנינו GUI באמצעות python ע"י שימוש בספריית tkinter בשביל הגרפיקה ובספריית sqlalchemy בשביל התקשורת עם בסיס הנתונים.
מפאת המקום (כ-1700 שורות) לא נראה את הקוד, אך נדגים את פעולותיו ונראה את התוצר הסופי.


### 5.1 מסך בית
אנחנו יצרנו 4 ממשקים בשביל המשתמשים השונים בבסיס הנתונים, כל אחד "מסתכל" על המידע הרלוונטי עבורו: ממשק עבור הדייר, ממשק עבור תחזוקה, ממשק עבור המשפחה של הדייר וממשק עבור המנהל.

![image](https://github.com/user-attachments/assets/351e47da-ef42-4069-af37-5fbf4fe323a4)


### 5.2 resident view

![image](https://github.com/user-attachments/assets/350375f0-8d99-4097-b287-38498a2bb4b3)


בממשק זה אנו מצריכים את הדייר להיכנס למערכת (signin) ומאפשרים לו לצפות בפעילויות הפופולריות, בפעילויות המומלצות עבורו ונותנים לו את האפשרות להירשם לפעילויות או לבטל הרשמה.

![image](https://github.com/user-attachments/assets/7cce60ab-4646-470d-b642-8925dee6fb71)


כמו שניתן לראות, דייר בעל ת.ז. 123 נכנס למערכת ומופיעים עבורו הפעילויות אליהם הוא רשום, הפעילויות המומלצות עבורו, טופ 5 פעילויות פופולריות וכן הבקשות תחזוקה שביצע.


בנוסף לכך, נותנים לו אפשרות לבצע בקשת תחזוקה עבור החדר שבו הוא גר (הוא גם יכול לראות את הבקשות שביצע כבר)


### 5.3 janitor view

![image](https://github.com/user-attachments/assets/8a835bae-085a-48b4-a27d-fd9c9b1fb450)


בממשק זה אנו מצריכים את איש התחזוקה להיכנס למערכת (signin) ומאפשרים לו לצפות בבקשות התחזוקה שהוא יוכל לשייך אליו, לצפות בבקשות שכבר משויכות אליו (עם בר שמראה את ההתקדמות) ולראות את כל הפריטים הקיימים במלאי ולהפחית את הכמות במידה והוא השתמש בחלק מהפריטים.

![image](https://github.com/user-attachments/assets/a72ddd0f-8fd0-4aa5-9a4f-ceaf50fdd3f8)

לאחר שאיש התחזוקה בעל הת.ז. 604 נכנס, הוא יכול לראות את הבקשות תחזוקה שמשויכות אליו (ניתן גם לראות את בר ההתקדמות), את הבקשות שעדיין לא משויכות לאף אחד והוא יכול לקחת עליהם אחריות ובכך לעדכן את בסיס הנתונים.
בנוסף הוא גם יכול לראות את המלאי של כל הפריטים ובמידת הצורך לעדכן כמויות מסוימות של פריטים וכך לעדכן את בסיס הנתונים.

### 5.4 family view

![image](https://github.com/user-attachments/assets/8f2ca0be-6cca-48f8-b199-63332bf7a153)

בממשק זה אנו מצריכים את בן המשפחה להיכנס למערכת (signin) ומאפשרים לו לצפות במידע הרלוונטי על הדייר: את היסטוריית הטיפולים הרפואיים ואת הצוות הרפואי שמטפל בדייר.

![image](https://github.com/user-attachments/assets/d51abbf7-24c2-4826-a825-6a77ddc6ddab)

כפי שניתן לראות, הוא יכול לראות את המידע הרלוונטי על הדייר.

### 5.5 manager view

בממשק זה צריך להיכנס עם שם משתמש וסיסמה של המנהל על מנת לראות את הגרפים שמתארים ביצועים של בית האבות.

![image](https://github.com/user-attachments/assets/8e90e1ed-dc18-4975-86c7-6dd65c686a78)

לאחר שהמנהל נכנס, ישנם כמה גרפים שהוא מסוגל לראות: אחוזים של השתתפות בפעילויות, השתתפות לאורך זמן, כמות התפוסה של החדרים בבית האבות, leaderboard של העובדים החרוצים בתחומם (נמדד ע"פ מספר הבקשות שביצעו) וכמות החדרים באחוזים עם מספר תלונות גבוה.

![image](https://github.com/user-attachments/assets/ad0563a7-0d95-45fd-8749-79544fee1258)


![image](https://github.com/user-attachments/assets/b4961c2e-14e0-4f27-bb57-e0d3d20e22d5)


