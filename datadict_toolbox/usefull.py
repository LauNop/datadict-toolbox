usefull_dict ={
  "Keywords": [
    "SELECT",
    "FROM",
    "WHERE",
    "GROUP BY",
    "HAVING",
    "ORDER BY",
    "JOIN",
    "INNER JOIN",
    "LEFT JOIN",
    "LEFT OUTER JOIN",
    "RIGHT JOIN",
    "RIGHT OUTER JOIN",
    "FULL JOIN",
    "UNION",
    "DISTINCT",
    "AS",
    "COUNT",
    "SUM",
    "AVG",
    "MIN",
    "MAX",
    "BETWEEN",
    "LIKE",
    "IN",
    "IS NULL",
    "IS NOT NULL",
    "LIMIT",
    "OFFSET",
    "ASCIICOMPARE",
    "COALESCE",
    "CASE",
    "CAST",
    "ON"
  ],
  "Multidim": [
    "ATTRIBUTE_NAME",
    "NOM_EXPLICIT",
    "DATA_TYPE",
    "IS_CALCULATED",
    "IS_MEASURE",
    "IS_DIMENSION",
    "EXPRESSION",
    "IS_VISIBLE",
    "GROUP",
    "CUBE_NAME",
    "CATALOG_NAME",
    "SOURCE"
  ],
  "Tabular": [
    "COLUMN_NAME",
    "NOM_EXPLICIT",
    "DATA_TYPE",
    "IS_CALCULATED",
    "IS_MEASURE",
    "EXPRESSION",
    "IS_VISIBLE",
    "TABLE_NAME",
    "CUBE_NAME",
    "CATALOG_NAME",
    "SOURCE"
  ],
  "Select_Dict": [
    "ALIAS_NAME",
    "COLUMN_NAME_OR_EXPRESSION",
    "TABLE_NAME",
    "TABLE_DESTINATION"
  ],
  "System_message": "You're an SQL developper who can extract all the initial columns, their alias and omit the intermediate aliases, their initial table and put them into a python list of dictionnary, without any comment. The user will show you how to handle specific cases as expression, * keyword and others with few examples then you'll analyse the given query. No comment only the 'Output:' then your list.",
  "Example_prompts":{
    "query":[
      """select AvionID, Pilote as Employee, Cargo as nbr_passengers, local as aeroport from APT.avion
""",
      """select 1 as magasin, a.numa as NumArticle, b.tt as typeTransport, a.valdef as valeurDefaut, from (\nselect * from MAG.maq)a\nleft join \n(select TT_TRANSIT as tt from TR.maq)b\non a.transit = b.transit
""",
      """select cast(ori||coda||caaa as nvarchar2(20)) as CodeActionCo1\n, case when caaa='18' or caaa='mb'  then cast(regexp_replace(cast(ori||coda||caaa as nvarchar2(20)), '[abcdefghijklmnopqrstuvwxyz]', '*') as nvarchar2(20)) \nelse cast(ori||coda||caaa as nvarchar2(20)) end as CodeActionCo\n, cast(lab as nvarchar2(50))as LibelleActionCo \nfrom SALAMAN.GAOKAO
""",
      """select * from TRAIN
""",
      """select a.* , macoto from (select AvionID, Pilote as Employee, Cargo as nbr_passengers, local as aeroport from APT.avion)a join BUZ
"""
    ],
    "solutions":[
      """[{"column":"AvionID","alias":"None","table":"APT.avion"},{"column":"Pilote","alias":"Employee","table":"APT.avion"},{"column":"Cargo";"alias":"nbr_passengers","table":"APT.avion"},{"column":"local","alias":"aeroport","table":"APT.avion"}]""",
      """[{"column":"value = 1","alias":"magasin","table":"None"},{"column":"numa","alias":NumArticle,"table":"MAG.maq"},{"column":"TT_TRANSIT","alias":typeTransport,"table":"TR.maq"},{"column":"valdef","alias":"valeurDefaut","table":"MAG.maq"}]""",
      """[{"column":"cast(ori||coda||caaa as nvarchar2(20))","alias":"CodeActionCo1","table":"SALAMAN.GAOKAO"},{"column":"case when caaa='18' or caaa='mb'  then cast(regexp_replace(cast(ori||coda||caaa as nvarchar2(20)), '[abcdefghijklmnopqrstuvwxyz]', '*') as nvarchar2(20)) \nelse cast(ori||coda||caaa as nvarchar2(20)) end","alias":"CodeActionCo","table":"SALAMAN.GAOKAO"},{"column":"cast(lab as nvarchar2(50))","alias":"LibelleActionCo","table":"SALAMAN.GAOKAO"}]""",
      """[{"column":"*","alias":"None","table":"TRAIN"}]""",
      """[{"column":"AvionID","alias":"None","table":"APT.avion"},{"column":"Pilote","alias":"Employee","table":"APT.avion"},{"column":"Cargo";"alias":"nbr_passengers","table":"APT.avion"},{"column":"local","alias":"aeroport","table":"APT.avion"},{"column":"macoto","alias":"None","table":"BUZ"]"""
    ]
  }
}