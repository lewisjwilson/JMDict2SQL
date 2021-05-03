# JMDict2SQL

### Description

A script to convert the JMDict_e.gz gzip file into a usable sqlite3 database

#### Prerequisites

- python3
- JMDict_e.gz file (avaliable from [edrdg.org](https://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project))

### JMdict_e.db Format

JMdict_e.db is a fully relational database.
The format for the database tables is as follows:

##### Entry Table

- `entry` [ **(PK) entry id** ]
  - `entry_id`: a unique ID for each entry
 
 
##### Kanji Tables

- `kanji` [ **(PK) id, (FK) entry_id, value** ]
  - `id`: a unique ID for each kanji
  - `entry_id`: foreign key from `entry` table
  - `value`: kanji value for the entry

- `kanji_tags` [ **(PK) id, (FK) kanji_id, value** ]
  - `id`: a unique ID for each kanji_tag record
  - `kanji_id`: foreign key from `kanji` table
  - `value`: info related to the associated kanji

- `kanji_common` [ **(PK) id, (FK) kanji_id, value** ]
  - `id`: a unique ID for each kanji_common record
  - `kanji_id`: foreign key from `kanji` table
  - `value`: denotes how common a kanji is



##### Kana Tables

- `kana` [ **(PK) id, (FK) entry_id, value, no_kanji** ]
  - `id`: a unique ID for each kana
  - `entry_id`: foreign key from `entry` table
  - `value`: kanji value for the entry
  - `no_kanji`: if 0, the kana is not the true reading of the kanji

- `kana_tags` [ **(PK) id, (FK) kana_id, value** ]
  - `id`: a unique ID for each kana_tag record
  - `kana_id`: foreign key from `kana` table
  - `value`: info related to the associated kana

- `kana_common` [ **(PK) id, (FK) kana_id, value** ]
  - `id`: a unique ID for each kana_common record
  - `kana_id`: foreign key from `kana` table
  - `value`: denotes how common a kana is

- `kana_applies_to_kanji` [ **(PK) id, (FK) kana_id, value** ]
  - `id`: a unique ID for each kana_applies_to_kanji record
  - `kana_id`: foreign key from `kana` table
  - `value`: denotes the kanji applies to the current kana



##### Sense Tables

- `sense` [ **(PK) id, (FK) entry_id** ]
  - `id`: a unique ID for each sense
  - `entry_id`: foreign key from `entry` table


 




### Usage

Run "setup.sh" to create an sqlite3 database (JMdict_e.db)
