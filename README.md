DISE Dashboard
===============

Dashboard for Dise data to allow interactive dise data gathering

New OLAP API Alpha Endpoint
---
Base URL: `http://host:port/api/v1/olap/`

Obtain and restore the database and point to it from local settings file to test.

Accepted parameters:

| name   | required |  description                    |
| ------ | ---------| ------------                    |
| method | yes | Name of one of the available mathods  |
| session | yes | Educational year (Available: `10-11` & `11-12`, Default `10-11`)  |

And you may also pass the parameters of respective method in the url.

Methods
---
 - School
    - School.getInfo
    - School.search
 - Cluster
    - Cluster.getInfo
    - Cluster.search

Methods: `School`
---
 - `School.getInfo`

Accepted parameters:

| name   | required |  description                    |
| ------ | ---------| ------------                    |
| code   | yes | DISE Code |

E.g. `http://local.dise.klp.org.in:8000/api/v1/olap/?method=School.getInfo&code=29010200101&session=10-11`

- `School.search`

Accepted parameters:

| name   | required |  description                    |
| ------ | ---------| ------------                    |
| limit   | no | maximum number of results to return |
| geo   | no | if the school has geo location, `true` or `false` |
| cluster   | no | name of cluster to search within |

E.g. To find maximum 50 schools in Mahagaon cluster that has no geolocation - `http://local.dise.klp.org.in:8000/api/v1/olap/?method=School.search&session=10-11&limit=50&cluster=MAHAGAON&geo=false`


Methods: `Cluster`
---
 - `Cluster.getInfo`

Accepted parameters:

| name   | required |  description                    |
| ------ | ---------| ------------                    |
| name   | yes | cluster name |

- `Cluster.search`

Accepted parameters:

| name   | required |  description                    |
| ------ | ---------| ------------                    |
| name   | no | name of cluster to search for |
| block   | no | name of block to search for the cluster |

E.g. `local.dise.klp.org.in:8000/api/v1/olap/?method=Cluster.search&session=10-11&name=DONGAON`


Backing up and restoring database
---
This is what I do as of now. For backing up -

    pg_dump -Ox -h localhost -U klp klpdise_olap > klp/dise/backups/klpdise_olap-2013-11-08-0241-full.pgsql

For restoring the same -

    sudo psql -U klp -h localhost klpdise_olap < klpdise_olap-2013-11-08-0241-full.pgsql

Indicators
---

1. General
    - Rural
    - Urban
    - Government
    - Private

2. Facility (negatives only)
    - Without Pucca Building
    - Classrooms needing repair
    - Without Toilets
    - Without Girls Toilets
    - Without Electricity
    - Without Secure Wall
    - Without Mid-Day-Meal
    - Without Drinking Water
    - Without Medical Checkup
    - Without Library
    - Without Blackboard
    - Without Playground
    - Without Ramps

3. Teachers
    - Without separate room for HM
    - Without HM

4. RTE
    - Without SDMC Constituted
    - Without SDMC Meetings
    - Without Text Books
    - With Children from Weaker Section Enrolled (PVT only)

5. Compound Indicators
    - With enrolment < 25
    - With PTR > 35
    - With Girls:Boys Gender ratio < 1

6. Range Indicators
    - With the number of class rooms between [___] and [___]
    - With the number of Teacher between [___] and [___]
    - With number of girls in class [____] between [____] and [____]
    - With number of boys in class [____] between [____] and [____]