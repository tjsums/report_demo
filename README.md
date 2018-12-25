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
- Meta文件：描述报表相关定义（基本信息、过滤、预加载等）
- 模板文件：Excel文件，承载样式、公式等

Meta文件样例如下：
- is_publish：是否发布
- name：报表名称，公司下不能重复
- headerLine：表头隐藏（view模式下隐藏的行数）
- number：报表ID，公司下不能重复
- filter：报表过滤定义，格式为hcForm格式，字段的Key值可以选择系统预制的CURRENT_DATE或者CURRENT_DEPARTMENT，这样在写公式的时候，相关参数可以忽略
- category：发布的模块ID
- data：预加载块数据，报表会首先计算预加载块数据，然后报表中LIST公式可以展开data
    - source：数据块公式
    - index_id：索引字段（data支持多个子数据块，数据块根据index_id合并成一个数据块）
    - childs：子数据块，通过index_id合并到数据块，key值改为childkey+"_" + 原key


```json
{
  "is_publish": true,   
  "name": "Flex报表演示", 
  "description": "演示Flex报表能力",
  "headerLine": 4,
  "number": "demo_suitongjian",
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

模板公式说明
------
- LIST：展开数据块，同行的值进行宏替换，如"{id}"将被填充为对应的ID，"[EMP_INFO({emp_id})]"也将被进行宏替换
- 相对单元格：引入了相对单元格概念，单元格取数或者一些统计函数如CELL_DIV等支持相对单元格取数
- 取消了对Excel公式的支持，Excel公式需要重新实现，现在实现了CELL_DIV和RANGE_SUM
    - CELL_DIV：单元格相除，如 CELL_DIV((0,-2),(0,-1)) 返回当前单元格同行的前移2格的值与前移1格的值相除
    - RANGE_SUM：区域汇总

云函数公式说明
------
第三代报表增加了对云函数自定义公式的支持：
- 云函数Key为FlexFormula_函数名称
- 云函数内容为一个继承自BaseFormulaObject的Class定义，其中do为函数体


部署说明
------
用户可以在报表平台新建报表，上传模板、定义Meta，也可以通过Github工程进行部署，本工程为部署工程样例，可以直接进行部署
- report 目录：存储报表定义
    - xxx.json：xxx报表的meta定义
    - template_xxx.xlsx：xxx报表的模板
- function 目录：云函数
