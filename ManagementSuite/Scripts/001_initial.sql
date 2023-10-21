CREATE TABLE Announcements
	(
	AnnouncementId bigint NOT NULL,
	Name nvarchar NOT NULL,
    Description nvarchar NULL,

	CONSTRAINT PK_Announcements PRIMARY KEY
	(
		AnnouncementId ASC
	)
)
