create_sqls = {
    'pa_stations_human_record_enc': '''
CREATE TABLE bi_papapa.pa_stations_human_record_enc (
`stid` int(6) NOT NULL AUTO_INCREMENT COMMENT '油站id',
`name` varchar(99) DEFAULT NULL COMMENT '油站名',
`st_human` varchar(26) DEFAULT NULL COMMENT '油站法人',
`address` varchar(199) DEFAULT NULL COMMENT '油站地址',
`province` varchar(41) DEFAULT NULL COMMENT '所在省份',
`create_time` datetime DEFAULT NULL COMMENT '创建时间',
`update_time` datetime DEFAULT NULL COMMENT '更新时间',
`muchcols_stid` int(6) DEFAULT NULL COMMENT '关联到大全表(much_cols)的stid',
`muchcols_name` varchar(255) DEFAULT NULL COMMENT '关联到大全表(much_cols)的name',
`min_sim` int(4) DEFAULT NULL COMMENT '两者名字字符串的最小变换步数，越小越相似，0表示完全相等。',
`obligate` text COMMENT '预留text',
PRIMARY KEY (`stid`),
UNIQUE KEY `NAME` (`name`),
KEY `IDX_UPD_TIME` (`update_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=104828 DEFAULT CHARSET=utf8 COMMENT='油站大全,人工录入版';
''',
    'pa_stations_muchcols_enc': '''
create table IF NOT EXISTS bi_papapa.pa_stations_muchcols_enc (
stid int(6) primary key not null auto_increment COMMENT '油站id' ,
name varchar(99) DEFAULT NULL COMMENT '油站名',
st_human varchar(26) DEFAULT '' COMMENT '油站法人',
address varchar(199) DEFAULT '' COMMENT '油站地址',
province varchar(43) DEFAULT '' COMMENT '所在省份',
city varchar(33) DEFAULT '' COMMENT '所在城市',
region varchar(33) DEFAULT '' COMMENT '区县',
phone varchar(66) DEFAULT '' COMMENT '电话',
email varchar(99) DEFAULT '' COMMENT '邮箱',
establish_date date DEFAULT 0 COMMENT '成立日期',
registered_capital varchar(39) DEFAULT '' COMMENT '注册资本',
register_num varchar(39) DEFAULT '' COMMENT '工商注册号',
organization_code varchar(39) DEFAULT '' COMMENT '组织代码',
Tax_identification varchar(39) DEFAULT '' COMMENT '纳税识别号',
home_page varchar(199) DEFAULT '' COMMENT '企业网址',
company_category varchar(30) DEFAULT '' COMMENT '公司类型',
operation_Scope text DEFAULT NULL COMMENT '经营范围',
status int(3) DEFAULT 0 COMMENT '企业状态 在业/存续 吊销 注销 迁出' ,
latitude double(20,6) DEFAULT 0 COMMENT '纬度',
longitude double(20,6) DEFAULT 0 COMMENT '经度',
confidence int(4) DEFAULT 0 COMMENT '置信度，描述打点准确度，大于80表示误差小于100m。该字段仅作参考，返回结果准确度主要参考precise参数。',
precise int(4) DEFAULT 0 COMMENT '1为精确查找，即准确打点',
p_carnum double(20,6) DEFAULT 0 COMMENT '5km范围内车辆数估计',
create_time datetime DEFAULT NULL COMMENT '创建时间',
update_time datetime DEFAULT NULL COMMENT '更新时间',
obligate text DEFAULT NULL COMMENT '预留text',
UNIQUE KEY `NAME` (`name`),
KEY `IDX_UPD_TIME` (`update_time`) USING BTREE
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='油站大全,主要结果表';
''',
    'pa_stations_juhe_enc': '''
create table IF NOT EXISTS bi_papapa.pa_stations_juhe_enc (
stid int(6) primary key not null auto_increment COMMENT '油站id' ,
name varchar(99) DEFAULT NULL COMMENT '油站名',
address varchar(199) DEFAULT '' COMMENT '油站地址',
fullregion varchar(33) DEFAULT '' COMMENT '省市区',
brandname varchar(30) DEFAULT '' COMMENT '公司品牌',
shoptype varchar(30) DEFAULT '' COMMENT '',
latitude double(20,6) DEFAULT 0 COMMENT '纬度',
longitude double(20,6) DEFAULT 0 COMMENT '经度',
create_time datetime DEFAULT NULL COMMENT '创建时间',
update_time datetime DEFAULT NULL COMMENT '更新时间',         
fwlsmc text DEFAULT NULL COMMENT '',
UNIQUE KEY `NAME_r` (`name`,`fullregion`),
KEY `name` (`name`),
KEY `IDX_UPD_TIME` (`update_time`) USING BTREE
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='聚合数据-油站大全';
''',
    'pa_city_property': '''
create table IF NOT EXISTS bi_papapa.pa_city_property (
cityid int(4) primary key not null auto_increment COMMENT '城市id' ,
cityname varchar(99) DEFAULT NULL COMMENT '城市名',
province varchar(99) DEFAULT NULL COMMENT '',
latitude double(20,6) DEFAULT 0 COMMENT '城市纬度(百度)',
longitude double(20,6) DEFAULT 0 COMMENT '城市经度(百度)',
property int(11) DEFAULT NULL COMMENT '属性(按位存储) 由低到高位分别表示：X(0-沿海|1-内地);XX(00-一线城市|01-二线|10-三线|11-其他); 有新维度向高位补充',  
create_time datetime DEFAULT NULL COMMENT '创建时间',
update_time datetime DEFAULT NULL COMMENT '更新时间',
obligate text DEFAULT NULL COMMENT '预留text',
UNIQUE KEY `NAME` (`cityname`),
KEY `IDX_UPD_TIME` (`update_time`) USING BTREE
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='城市属性表';
'''
}




