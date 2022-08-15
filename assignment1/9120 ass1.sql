DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Journeys;
DROP TABLE IF EXISTS Vehicle;
DROP TABLE IF EXISTS Participate;
DROP TABLE IF EXISTS Run;
DROP TABLE IF EXISTS Participants;
DROP TABLE IF EXISTS Officials;
DROP TABLE IF EXISTS Person;
DROP TABLE IF EXISTS SportingEvents;
DROP TABLE IF EXISTS Venue;
DROP TABLE IF EXISTS Accommodation;
DROP TABLE IF EXISTS Location;


--As refer to the requirement in assignment1, detailed information of Location should all be NOT NULL, what’s more, CHECK in BuiltCost is to ensure cost more than nil.
CREATE TABLE Location(
    LocationId	  CHAR (5)       PRIMARY KEY,
	LocationName  VARCHAR (100)  NOT NULL UNIQUE ,
	Longitude     DECIMAL (9,6)	 NOT NULL,
	Latitude      DECIMAL (8,6)	 NOT NULL,
	BuiltDate     DATE			 NOT NULL,
	Suburb        VARCHAR (20)   NOT NULL,
	Area          VARCHAR (20)   NOT NULL,
	Address       VARCHAR (100)  NOT NULL,
	BuiltCost     DECIMAL (30,4) NOT NULL CHECK (BuiltCost > 0)
);


--ON DELETE CASCADE is used to keep the synchronization between the subclass and the superclass, and to avoid error reporting.
CREATE TABLE Accommodation(
	LocationId  CHAR (5) PRIMARY KEY,
	FOREIGN KEY (LocationId) REFERENCES Location(LocationId) ON DELETE CASCADE
);


CREATE TABLE Venue( 
    LocationId  CHAR (5) PRIMARY KEY,
	FOREIGN KEY (LocationId) REFERENCES Location(LocationId) ON DELETE CASCADE
);


--As refer to the requirement in assignment1, all elements related to Name, Time and Date should be NOT NULL. Besides, CHECK in ResultType is used to make sure that ResultType is either “Time-based” and “Score-bases”.
CREATE TABLE SportingEvents(
	EventId       VARCHAR (10)   PRIMARY KEY,
	LocationId	  CHAR (5),
	SportName     VARCHAR (20)   NOT NULL,
	EventName     VARCHAR (50)   NOT NULL,
	Time          TIME			 NOT NULL,
	Date          DATE			 NOT NULL,
	ResultType    VARCHAR (15)   NOT NULL CHECK (ResultType IN ('Time-based','Score-based')),
	FOREIGN KEY   (LocationId)   REFERENCES Venue (LocationId) ON DELETE CASCADE
);


--As refer to the requirement in assignment1, all elements related to Name, Time and Date should be NOT NULL. We also decided that each person should have a clear and NOT NULL HomeCountry. Besides, CHECK in Gender is used to make sure that Gender is either “Male”,“Female” and “Other”.
CREATE TABLE Person( 
	PersonId    VARCHAR (10)    PRIMARY KEY, 
	LocationId  CHAR (5),
	Email       VARCHAR (50)	UNIQUE NOT NULL, 
	Gender      VARCHAR (10)    NOT NULL CHECK (Gender IN ('Male','Female','Other')), 
	FirstName   VARCHAR (20)    NOT NULL,
	LastName    VARCHAR (20)    NOT NULL,
	DOB         DATE			NOT NULL,
	HomeCountry VARCHAR (20)    NOT NULL,
	Age         INTEGER,
	FOREIGN KEY (LocationId)    REFERENCES Accommodation (LocationId) ON DELETE CASCADE
); 


--CHECK in duty is used to make sure that officials’ duty can be only considered through “Referee games”, “Judge performance” and “Awarding medals” as state in assignment 1.
CREATE TABLE Officials( 
	PersonId    VARCHAR (10)   PRIMARY KEY,
	Duty        VARCHAR (20)   CHECK (Duty IN ('Referee games','Judge performance','Awarding medals')),
	FOREIGN KEY (PersonId) REFERENCES Person(PersonId) ON DELETE CASCADE
); 


CREATE TABLE Participants( 
	PersonId        VARCHAR (10) PRIMARY KEY, 
	BirthCountry    VARCHAR (20), 
	ParticipantType VARCHAR (20),
	FOREIGN KEY (PersonId) REFERENCES Person(PersonId) ON DELETE CASCADE
); 


CREATE TABLE Run( 
	PersonId  VARCHAR (10), 
	EventId   VARCHAR (10),
	FOREIGN KEY (PersonId) REFERENCES Officials(PersonId)     ON DELETE CASCADE,
	FOREIGN KEY (EventId)  REFERENCES SportingEvents(EventId) ON DELETE CASCADE
); 


CREATE TABLE Participate( 
	PersonId  VARCHAR (10),  
	EventId   VARCHAR (10),
	Rank      INTEGER,
	Result    VARCHAR (20),
	FOREIGN KEY (PersonId) REFERENCES Participants(PersonId)  ON DELETE CASCADE,
	FOREIGN KEY (EventId)  REFERENCES SportingEvents(EventId) ON DELETE CASCADE
);


--CHECK in Type is used to make sure that Vehicles’ type can be only considered as one of the type in  “Van”, “Minibus” and “Bus” as required in assignment 1.
CREATE TABLE Vehicle (
	Code       VARCHAR (20) PRIMARY KEY,
	Type       VARCHAR (10) CHECK (Type IN ('Van','Minibus','Bus')),
	Capacity   Integer      NOT NULL CHECK (Capacity > 0 and Capacity<=23)
);


--As refer to the requirement in assignment1, all elements related to Name, Time and Date should be NOT NULL.
CREATE TABLE Journeys (
	DepartureTime TIME          NOT NULL,
	ArrivalTime   TIME   	    NOT NULL,
	Date          DATE 		    NOT NULL,
	Departure     CHAR (5)      NOT NULL,
	Arrival       CHAR (5)  	NOT NULL,
	Code          VARCHAR (20)  NOT NULL,
	PRIMARY KEY (Code, DepartureTime, Date),
	FOREIGN KEY (Departure) REFERENCES Location(LocationId) ON DELETE CASCADE,
	FOREIGN KEY (Arrival)   REFERENCES Location(LocationId) ON DELETE CASCADE,
	FOREIGN KEY (Code)   	REFERENCES Vehicle (Code) 		ON DELETE CASCADE
);


--As refer to the requirement in assignment1, all elements related to Name, Time and Date should be NOT NULL.
CREATE TABLE Books (
	PersonId 		VARCHAR (10) 	NOT NULL,
	DepartureTime 	TIME 			NOT NULL,
	Date 			DATE 			NOT NULL,
	Code  			VARCHAR (20)	NOT NULL,
	PRIMARY KEY (PersonId, DepartureTime, Date, Code),
	FOREIGN KEY (PersonId)       		   REFERENCES Person   (PersonId) 	 ON DELETE CASCADE,
	FOREIGN KEY (DepartureTime,Date,Code)  REFERENCES Journeys (DepartureTime,Date,Code) ON DELETE CASCADE
);

--INSERT statements to populate each relation with at least two records.
INSERT INTO Location VALUES ('0001','Fortitude Valley', '153.0281', '-27.4679', '2012-08-08', 'Brisbane City', 'QLD', 'Soleil, 485 Adelaide St', '25000000');
INSERT INTO Location VALUES ('0002','Jie Valley', '152.081', '-25.679', '2016-06-06', 'Zetland', 'NSW', '22 Barr St', '66000000');
INSERT INTO Location VALUES ('0003','Lin Valley', '152.564', '-26.549', '2017-07-07', 'Waterloo', 'QLD', '6 Ali St', '43000000');
INSERT INTO Location VALUES ('0004','Liu Valley', '152.024', '-24.645', '2018-08-08', 'Ultimo', 'NSW', '66 Tin St', '64000000');
INSERT INTO Accommodation VALUES ('0003');
INSERT INTO Accommodation VALUES ('0004');
INSERT INTO Venue VALUES ('0001');
INSERT INTO Venue VALUES ('0002');
INSERT INTO SportingEvents VALUES ('1', '0001', 'Basketball', '3x3 Basketball', '10:00:00', '2024-08-10', 'Score-based');
INSERT INTO SportingEvents VALUES ('2', '0002', 'Running', '100m Running', '10:00:00', '2024-08-12', 'Time-based');
INSERT INTO Person VALUES ('1', '0003', 'tom136@gmail.com', 'Male', 'Tom', 'Potter', '2000-07-16', 'Australia', '24');
INSERT INTO Person VALUES ('2', '0004', 'harry857@gmail.com', 'Female', 'Harry', 'Potter', '2006-08-25', 'Britain', '18');
INSERT INTO Officials VALUES ('1', 'Referee games');
INSERT INTO Officials VALUES ('2', 'Awarding medals');
INSERT INTO Participants VALUES ('1', 'Australia', 'Athlete');
INSERT INTO Participants VALUES ('2', 'Britain', 'Athlete');
INSERT INTO Run VALUES ('1', '1');
INSERT INTO Run VALUES ('2', '2');
INSERT INTO Participate VALUES ('1','2',1,'10''18"');
INSERT INTO Participate VALUES ('2','1',1,'10');
INSERT INTO Vehicle VALUES ('A1','Van',22);
INSERT INTO Vehicle VALUES ('B2','Bus',15);
INSERT INTO Journeys VALUES ('08:00:00','09:00:00','2024-08-12','0001','0002','A1');
INSERT INTO Journeys VALUES ('18:00:00','19:00:00','2024-08-12','0002','0001','B2');
INSERT INTO Books VALUES ('1','08:00:00','2024-08-12','A1');
INSERT INTO Books VALUES ('2','18:00:00','2024-08-12','B2');