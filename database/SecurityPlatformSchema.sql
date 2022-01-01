create table client
  	(ID 			serial,
   	 name			varchar(20),
   	 email		varchar(40),
 	 hash_value	varchar(64),
  	 primary key (ID)
 	);
 
create table role
	(role_ID		serial,
  	 role_name	varchar(20) unique,
  	 primary key (role_ID)
 	);

create table role_right
  	(role_name	varchar(20),
  	 object		varchar(20),
  	 access_right	varchar(20),
  	 primary key (role_name, object, access_right),
  	 foreign key (role_name) references role(role_name)
  	);
  
create table criteria 
  	(criteria_ID		serial,
  	 criteria_name	varchar(20),
  	 comment			varchar(100),
   	 primary key	(criteria_ID)
  	);
  
create table evidence
	(evidence_ID		serial,
	 name			varchar(20),
	 project_name		varchar(20),
	 create_date_time	timestamp,
	 last_edit_time		timestamp,
	 comment		varchar(100),
	 path			varchar(2083),
	 primary key (evidence_ID)
	);

create table backup_evidence as
	(select * from evidence);

create table assign
	(client_ID	integer,
	 role_ID		integer,
	 primary key (client_ID, role_ID),
	 foreign key (client_ID) references client(ID)
		on delete cascade,
	 foreign key (role_ID) references role(role_ID)
	);

create table manage_criteria
	(role_ID		integer,
	 criteria_ID	integer,
	 primary key (role_ID, criteria_ID),
	 foreign key (criteria_ID) references criteria(criteria_ID),
	 foreign key (role_ID) references role(role_ID)	 
	);

create table contain
	(criteria_id		integer,
	 evidence_id		integer,
	 primary key (criteria_id, evidence_id),
	 foreign key (criteria_id) references criteria(criteria_ID),
	 foreign key (evidence_id) references evidence(evidence_ID)
	);

create table manage_evidence
	(role_ID		integer,
	 evidence_ID		integer,
	 primary key (role_ID, evidence_ID),
	 foreign key (evidence_ID) references evidence(evidence_ID),
	 foreign key (role_ID) references role(role_ID)
	);