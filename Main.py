import os

"""
with open(".env", "r") as f:
    for line in f.readlines():
        try:
            key, value = line.split('=')
            os.putenv(key, value)
        except ValueError:
            # syntax error
            pass
"""

if __name__ == "__main__":
    print("Hello World")
    string = """
["dcf_cdmag","dcf_nocdefou","cast(cdf_nobonliv as nvarchar2(20))","CDF_NORECEPT","cdf_cdfo","dcf_novar","cast(cdf_tydocu as nvarchar2(2))","sit_cdsitu","dcf_noart","dcf_qtcdee","cast(nvl(dcf_pdcdee,0) as float)","cast(nvl(DCF_QTGRATUI ,0) as float)","cast(nvl(dcf_qtrecp,0) as float)","cast(nvl(dcf_pdrecp,0) as float)","nvl(dcf_qtfact, 0)","dcf_qtmjst","case when dcf_qtmjst =0 then nvl(dcf_qtrecp,0) else 0 end","cast(dcf_tyunfac as nvarchar2(2))","dcf_pxtarif","cast(dcf_tyuvec as nvarchar2(2))","cast(case when nvl(CDF_MTREVREL,0)=0 then CDF_MTACHAT else CDF_MTREVREL end as float)","dcf_pxrvrlim","dcf_mttxbfht","dcf_pxrevien","dcf_pxnet","dcf_cffacvte","case when (to_char(cdf_dtcomman,'yyyy')>2000 and to_char(cdf_dtcomman,'yyyy')<2079) then cdf_dtcomman else null end","case when (to_char(cdf_dtlivr,'yyyy')>2000 and to_char(cdf_dtlivr,'yyyy')<2079) then cdf_dtlivr else null end","case when (to_char(cdf_dtrecept,'yyyy')>2000 and to_char(cdf_dtrecept,'yyyy')<2079) then cdf_dtrecept  else null end","dcf_pxvent","epmp_pxmoypdr","cast(cdf_noblfour as nvarchar2(25))","CDF_NORAPP","cast(REGEXP_REPLACE(RTRIM(LTRIM(CDF_CDDOSTST)),'\D','')as nvarchar2(25))","cast(cdf_cdimmatr as nvarchar2(20))","dcf_txtva","CAST(econ_cdtypect as nvarchar2(4))","TypeContainer"]
"""
print(string[1136:1140])


