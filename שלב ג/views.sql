-- caregiver_maintenance (maintenance_req & inventory & caregiver & room)
create view caregiver_maintenance as 
select c.caregiverid, (c.firstname || ' ' || c.lastname) caregiver_name, i.item_name, i.quantity, r.roomnumber, mr.request_id, mr.req_description, mr.req_status
from maintenance_req mr
join caregiver c on mr.staff_member_id = c.caregiverid
join inventory i on mr.item_id = i.item_id
join department d on c.departmentid = d.departmentid
join room r on mr.room_id = r.roomid
where d.name not ilike '%Care%' and d.name not ilike '%nursing%'

-- query 1	(find the items that need to restocked)

select item_name, quantity
from caregiver_maintenance
where quantity <= 15 and req_status != 'taken care of'

-- query 2	(find the requests that belong to a specific caregiver)
select req_description, req_status, roomnumber
from caregiver_maintenance
where caregiver_name = 'David Norman'


-- family (medical treatment & family visit)
create view family_view as 
select fv.visitdate, fv.visitorname, r.firstname || ' ' || r.lastname resident_name,
c.firstname || ' ' || c.lastname caregiver_name, c.phone caregiver_phone, mt.treatmentdate, mt.treatmenttype
from familyvisit fv
join medicaltreatment mt on mt.residentid = fv.residentid
join caregiver c on c.caregiverid = mt.caregiverid
join resident r on r.residentid = mt.residentid

-- query 1 (find details of a specific resident's doctor)
select caregiver_name, caregiver_phone, treatmenttype
from family_view
where resident_name = 'Natasha Decker'
group by caregiver_name, caregiver_phone, treatmenttype

-- query 2 (medical history)
select treatmentdate, treatmenttype
from family_view
where resident_name = 'Melissa Joseph'
order by treatmentdate
