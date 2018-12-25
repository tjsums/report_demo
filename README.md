HCM Cloud 第三代报表系统
======
特性
------
在第一代Excel模板基础上，重点优化一下几点：
* 取消对于Office Server的依赖，改为用openpyxl组件并加以包装，大幅度降低部署难度；提升运算性能与稳定性
* 在第一代基础上，将公式运算转移到进程内运算，降低RPC次数，提升性能与稳定性
* 结合第二代的优势，通过预加载List信息，及List合并，转换公式取数为批量取数，大幅度提升性能
* 增加参数支持
* 增加了自定义穿透的支持
* 增加对于动态模型统计的公式支持
* 增加基于云函数的自定义公式
* 增加了基于Github工程的部署

开发
------
一个报表由两部分组成：
* Meta文件：描述报表相关定义（基本信息、过滤、预加载等）
* 模板文件：Excel文件，承载样式、公式等

Meta文件样例如下：
```json
{
  "is_publish": true,   # 是否发布
  "name": "Flex报表演示", # 报表名称，公司下不能重复
  "description": "演示Flex报表能力",
  "headerLine": 4,     # 表头隐藏（view模式下隐藏的行数）
  "number": "demo_suitongjian", # 报表ID，公司下不能重复
  "filter": [
    {
      "component": "hc-selector-depart",
      "options": {
        "singleLine": true,
        "required": true,
        "role": "manager"
      },
      "key": "CURRENT_DEPARTMENT",
      "label": "部门名称"
    },
    {
      "component": "hc-input-datetime",
      "options": {
        "inputLock": true,
        "singleLine": true,
        "required": true,
        "format": "yyyy-MM-dd"
      },
      "key": "CURRENT_DATE",
      "label": "时间"
    }
  ],
  "category_id": 3,
  "data": {
    "emp_group": {
      "source": "EMP_GROUP()",
      "childs": {
        "emp_out_year": {
          "source": "EMP_OUT(CURRENT_DEPARTMENT,'Y')",
          "index_id": "id"
        },
        "emp_in_month": {
          "source": "EMP_IN(CURRENT_DEPARTMENT,'M')",
          "index_id": "id"
        },
        "emp_in_year": {
          "source": "EMP_IN(CURRENT_DEPARTMENT,'Y')",
          "index_id": "id"
        },
        "perf_data": {
          "source": "MODEL_COUNT('CustDepartPerf',None,'income','depart_id','month:2018-12')",
          "index_id": "depart_id"
        },
        "emp_out_month": {
          "source": "EMP_OUT(CURRENT_DEPARTMENT,'M')",
          "index_id": "id"
        }
      },
      "index_id": "id"
    }
  }
}


```


