select * from (
    select * from bibtex_entry where 
        key like '%/sigmod/%'
        and year in ('2014', '2015', '2016', '2017')
        limit 200
    )
    
UNION

select * from (
    select * from bibtex_entry where 
        key like '%/sbbd/%'
        and year in ('2014', '2015', '2016', '2017')
        limit 200
    )
    
UNION
    
select * from (
    select * from bibtex_entry where 
        key like '%/vldb/%'
        and year in ('2014', '2015', '2016', '2017')
        limit 200
    )
    
UNION
    
select * from (
    select * from bibtex_entry where 
        key like '%/icde/%'
        and year in ('2014', '2015', '2016', '2017')
        limit 200
    )

UNION

select * from (
    select * from bibtex_entry where 
        key like '%/www/%'
        and year in ('2014', '2015', '2016', '2017')
        limit 200
    )

-- sigmod
-- sbbd
-- cldb
-- icde
-- www