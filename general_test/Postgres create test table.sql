
DROP TABLE IF EXISTS "TestTable";

CREATE TABLE "TestTable"
(
  "RowID" serial NOT NULL,
  "NumberValue" integer NOT NULL,
  "TextDescription" character varying(500) NOT NULL
)
WITH (OIDS=FALSE);

ALTER TABLE "TestTable" OWNER TO postgres;

ALTER TABLE "TestTable"
ADD CONSTRAINT "PK_TestTable" PRIMARY KEY ("RowID");

INSERT INTO "TestTable" ("NumberValue", "TextDescription")
VALUES	(10, 'PRINT "Hello world!"'),
	(20, 'GOTO 10');

SELECT 	"RowID",
	"NumberValue",
	"TextDescription"
FROM 	"TestTable";
