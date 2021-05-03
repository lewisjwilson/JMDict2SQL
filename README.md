# JMDict2SQL

### Description

A script to convert the JMDict_e.gz gzip file into a usable sqlite3 database

#### Prerequisites

    - python3
    - JMDict_e.gz file (avaliable from edrdg.org)

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
  - `value`: denotesthat the kanji applies to the current kana



##### Sense Tables

- `sense` [ **(PK) id, (FK) entry_id** ]
  - `id`: a unique ID for each sense
  - `entry_id`: foreign key from `entry` table

- `sense_applies_to_kanji` [ **(PK) id, (FK) sense_id, value** ]
  - `id`: a unique ID for each sense_applies_to_kanji record
  - `sense_id`: foreign key from `sense` table
  - `value`: denotes that the sense applies to the current kanji

- `sense_applies_to_kana` [ **(PK) id, (FK) sense_id, value** ]
  - `id`: a unique ID for each sense_applies_to_kana record
  - `sense_id`: foreign key from `sense` table
  - `value`: denotes that the sense applies to the current kana

- `part_of_speech` [ **(PK) id, (FK) sense_id, value** ]
  - `id`: a unique ID for each record
  - `sense_id`: foreign key from `sense` table
  - `value`: denotes the part of speech of the sense (eg. noun, adjective...)


 
### ER Diagram

![JMdict_e_ER_diagram](https://user-images.githubusercontent.com/55784291/116845561-1a4bb700-ac21-11eb-8dc8-63f18a7772d9.png)
(ER Diagram created using [dbeaver.io](https://dbeaver.io/))

### Usage

1. Download the latest [JMdict_e.gz file](https://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project).
2. Run `./setup.sh` to create an sqlite3 database (JMdict_e.db)
3. Find the output `JMdict_e.db`
