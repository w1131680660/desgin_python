webpackJsonp([16],{JYJA:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=a("lHA8"),l=a.n(i),d=a("Gu7T"),s=a.n(d),o=a("mtWM"),n=a.n(o),r={data:function(){return{fileList:[],file:"",pageFlag:!1,pageShow:!0,selectItem:"",centerDialogVisible2:!1,centerDialogVisible:!1,leftNavData:[],tableList:[],addSite:"",addCountry:"",addProduct_code:"",addSpu:"",addSku:"",addState:"",addAsin:"",addFnsku:"",addUPC:"",addStardate:"",addenddate:"",addsellFlag:"",addsellLink:"",addoriginalLink:"",addplatform:"",editSite:"",editCountry:"",editProduct_code:"",editSpu:"",editSku:"",editState:"",editAsin:"",editFnsku:"",editUPC:"",editStardate:"",editenddate:"",editsellFlag:"",editsellLink:"",editoriginalLink:"",editplatform:"",stateList:[],productCodeList:[],dropProductCode:"",firstData:"",secondData:"",threeData:"",total:0,page:1,addProduct_codeList:[],editProduct_codeList:[],searchData:"",isShowSell:!1,isShowSell1:!1}},methods:{checkFileType:function(t){return!!/\.(xlsx|xls)$/g.test(t)},changeFile:function(t){var e=this;console.log(this.$refs.uploadExcel),console.log(t);var a=t.target.files[0];if(console.log(a),!this.checkFileType(a.name))return alert("请上传后缀为.xlsx或.xls文件！"),this.file="",void(this.fileList=[]);this.$refs.uploadExcel.value="",this.file=a;var i=this._url2+"server/databases/commodity_script/",l=new FormData;l.append("country",this.secondData),l.append("site",this.threeData),l.append("files",this.file),this.$axios.post(i,l).then(function(t){200===t.data.code?(e.$message.success("请求成功"),e.file="",e.fileList=[]):e.$message.warning("请求失败")})},clearSearchInfo:function(){this.dropProductCode="",this.searchData="",this.search()},requestData:function(t){var e=this,a=this._url2+"server/databases/commodity_check_time/";this.$axios.get(a,{params:{data_id:t}}).then(function(t){200===t.data.code?(alert("操作成功！"),e.search(e.page)):alert("操作未成功！")})},clickTr:function(t,e){var a=this.tableList[e].id;if(t.target.constructor===HTMLSpanElement)this.requestData(a);else{var i=document.querySelectorAll(".checkLI")[e];this.selectItem&&(this.selectItem.checked=!1),this.selectItem!==i?(this.selectItem=i,this.selectItem.checked=!0):this.selectItem=""}},getDefaultData:function(){var t=this;this.firstData="Amazon",this.secondData="美国",this.threeData="胤佑",n()({method:"get",url:this._url2+"server/databases/commodity_information",params:{platform:this.firstData,country:this.secondData,site:this.threeData,page:1}}).then(function(e){console.log(e),t.stateList=e.data.commodity_data,t.tableList=e.data.data,console.log("打印",t.tableList),t.tableList.forEach(function(e,a){"null"==e.commodity_state&&(t.tableList[a].commodity_state=""),"null"==e.upc&&(t.tableList[a].upc=""),"null"==e.begin_sell_date&&(t.tableList[a].begin_sell_date=""),"null"==e.over_sell_date&&(t.tableList[a].over_sell_date="")}),t.total=e.data.count_data[0].count_id,t.productCodeList=e.data.product_code_data,t.addProduct_codeList=e.data.product_code_data,t.editProduct_codeList=e.data.product_code_data})},NavClick:function(t,e,a){var i=this;console.log(t,e,a),this.firstData=t,this.secondData=e,this.threeData=a,this.dropProductCode="",n()({method:"get",url:this._url2+"server/databases/commodity_information",params:{platform:this.firstData,country:this.secondData,site:this.threeData,page:1}}).then(function(t){console.log(t),i.tableList=t.data.data,console.log("点击事件",i.tableList),i.tableList.forEach(function(t,e){"null"==t.commodity_state&&(i.tableList[e].commodity_state=""),"null"==t.upc&&(i.tableList[e].upc=""),"null"==t.begin_sell_date&&(i.tableList[e].begin_sell_date=""),"null"==t.over_sell_date&&(i.tableList[e].over_sell_date="")}),i.$nextTick(function(){$(".MN_table >tbody").scrollTop(0)}),i.productCodeList=t.data.product_code_data,console.log(t.data),console.log(i.productCodeList),i.total=t.data.count_data[0].count_id,i.page=1,i.searchData="";for(var e=document.querySelectorAll(".checkLI"),a=0;a<e.length;a++)e[a].checked=!1})},addNewdata:function(){this.centerDialogVisible=!0,console.log(this.tableList),this.addplatform=this.firstData,this.addCountry=this.secondData,this.addSite=this.threeData,this.addProduct_code="",this.addSpu="",this.addSku="",this.addState="",this.addAsin="",this.addFnsku="",this.addUPC="",this.addStardate="",this.addenddate="",this.addsellFlag="",this.addsellLink="",this.addoriginalLink=""},addReset:function(){this.addProduct_code="",this.addSpu="",this.addSku="",this.addState="",this.addAsin="",this.addFnsku="",this.addUPC="",this.addStardate="",this.addenddate="",this.addsellFlag="",this.addsellLink="",this.addoriginalLink=""},addSubmit:function(){var t=this;if(""==this.addSite||""==this.addCountry||""==this.addProduct_code||""==this.addplatform||""==this.addSpu||""==this.addSku||""==this.addState||""==this.addAsin||""==this.addFnsku||""==this.addStardate||""==this.addsellFlag||""==this.addoriginalLink)alert("请填写除UPC和停止销售时间外所有选项");else{this.centerDialogVisible=!1;var e=new FormData;e.append("site",this.addSite),e.append("country",this.addCountry),e.append("product_code",this.addProduct_code),e.append("platform",this.addplatform),e.append("spu",this.addSpu),e.append("sku",this.addSku),e.append("commodity_state",this.addState),e.append("asin",this.addAsin),e.append("fnsku",this.addFnsku),e.append("upc",this.addUPC),e.append("begin_sell_date",this.addStardate),e.append("over_sell_date",this.addenddate),e.append("select_link",this.addsellFlag),e.append("sku_link",this.addsellLink),e.append("product_link",this.addoriginalLink),this.$axios.post(this._url2+"server/databases/commodity_information",e).then(function(e){200==e.data.code?(alert("新增成功"),t.reloadTable("新增")):alert(e.data.msg)})}},deleteData:function(){for(var t=this,e=[],a=document.querySelectorAll(".checkLI"),i=0;i<a.length;i++)1==a[i].checked&&e.push(a[i].value);0===e.length?alert("请选中您想删除的数据"):this.$confirm("此操作将永久删除选中商品, 是否继续?","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){t.$axios.delete(t._url2+"server/databases/commodity_information",{params:{id:e}}).then(function(e){if(200==e.data.code){t.reloadTable("删除"),t.$message({type:"success",message:"删除成功!"});for(var a=document.querySelectorAll(".checkLI"),i=0;i<a.length;i++)a[i].checked=!1}})}).catch(function(){})},editSubmit:function(){var t=this;if(""==this.editSite||""==this.editCountry||""==this.editProduct_code||""==this.editplatform||""==this.editSpu||""==this.editSku||""==this.editState||""==this.editAsin||""==this.editFnsku||""==this.editStardate||""==this.editsellFlag||""==this.editoriginalLink)alert("请填写除UPC和停止销售时间外所有选项");else{this.centerDialogVisible2=!1;for(var e="",a=document.querySelectorAll(".checkLI"),i=0;i<a.length;i++)1==a[i].checked&&(e=a[i].value);var l=new FormData;l.append("id",e),l.append("site",this.editSite),l.append("country",this.editCountry),l.append("product_code",this.editProduct_code),l.append("platform",this.editplatform),l.append("spu",this.editSpu),l.append("sku",this.editSku),l.append("commodity_state",this.editState),l.append("asin",this.editAsin),l.append("fnsku",this.editFnsku),l.append("upc",this.editUPC),l.append("begin_sell_date",this.editStardate),l.append("over_sell_date",this.editenddate),l.append("select_link",this.editsellFlag),l.append("sku_link",this.editsellLink),l.append("product_link",this.editoriginalLink),this.$axios.put(this._url2+"server/databases/commodity_information",l).then(function(e){200==e.data.code&&(alert("修改成功"),console.log(t.page),t.reloadTable("编辑"))})}},openedit:function(){for(var t=document.querySelectorAll(".checkLI"),e=0,a=0;a<t.length;a++)1==t[a].checked&&(e++,this.editProduct_code=this.tableList[a].product_code,this.editSpu=this.tableList[a].spu,this.editSku=this.tableList[a].sku,this.editAsin=this.tableList[a].asin,this.editFnsku=this.tableList[a].fnsku,this.editUPC=this.tableList[a].upc,this.editStardate=this.tableList[a].begin_sell_date,this.editenddate=this.tableList[a].over_sell_date,this.editoriginalLink=this.tableList[a].product_link,this.editState=this.tableList[a].commodity_state,this.editsellFlag=this.tableList[a].select_link);1==e?(this.centerDialogVisible2=!0,this.editSite=this.tableList[0].site,this.editCountry=this.tableList[0].country,this.editplatform=this.tableList[0].platform,console.log(this.tableList)):alert("请只选择一个编辑")},search:function(t){var e=this;t||(this.page=1),n()({method:"get",url:this._url2+"server/databases/commodity_information",params:{platform:this.firstData,country:this.secondData,site:this.threeData,product_code:this.dropProductCode,condition:this.searchData,page:t||this.page}}).then(function(t){console.log(t),e.tableList=t.data.data;for(var a=document.querySelectorAll(".checkLI"),i=0;i<a.length;i++)a[i].checked=!1})},reloadEditTable:function(){var t=this;this.page=1,n()({method:"get",url:this._url2+"server/databases/commodity_information",params:{platform:this.firstData,country:this.secondData,site:this.threeData,product_code:this.dropProductCode,page:this.page}}).then(function(e){t.tableList=e.data.data,t.total=e.data.count_data[0].count_id})},reloadTable:function(t){var e=this;if(t&&"新增"===t){console.log("总条数",this.total);var a=Math.ceil((this.total+1)/50);Math.ceil(this.total/50)!==a&&(this.pageShow=!1,this.pageFlag=!0),this.page=a}else if(t&&"删除"===t){var i=this.total-1;console.log("删除后条数",i),console.log("总条数",this.total),i<50*this.page&&(this.page=Math.ceil(i/50))}n()({method:"get",url:this._url2+"server/databases/commodity_information",params:{platform:this.firstData,country:this.secondData,site:this.threeData,product_code:this.dropProductCode,page:this.page}}).then(function(t){console.log(t),e.tableList=t.data.data,e.total=t.data.count_data[0].count_id,e.$nextTick(function(){e.pageFlag&&(e.pageShow=!0)})})},addblo:function(){console.log(this.addsellFlag),"跟卖链接"==this.addsellFlag?this.isShowSell=!0:this.isShowSell=!1},editblo:function(){"跟卖链接"==this.editsellFlag?this.isShowSell1=!0:this.isShowSell1=!1},tagCheck:function(t){0==document.querySelectorAll(".checkLI")[t].checked?document.querySelectorAll(".checkLI")[t].checked=!0:document.querySelectorAll(".checkLI")[t].checked=!1},handleCurrentChange:function(t){var e=this;this.page=t,n()({method:"get",url:this._url2+"server/databases/commodity_information",params:{platform:this.firstData,country:this.secondData,site:this.threeData,page:this.page,condition:this.searchData,product_code:this.dropProductCode}}).then(function(t){console.log(t),e.tableList=t.data.data,e.$nextTick(function(){$(".MN_table >tbody").scrollTop(0)});for(var a=document.querySelectorAll(".checkLI"),i=0;i<a.length;i++)a[i].checked=!1})},addEnter:function(){this.addSubmit()},editEnter:function(){this.editSubmit()}},created:function(){var t=this;this.getDefaultData(),n()({url:this._url2+"server/personnel_management/area_sign2/",method:"get"}).then(function(e){t.leftNavData=e.data.data,console.log(t.leftNavData);var a=0;for(var i in t.leftNavData.Amazon)"英国"!=i&&"德国"!=i&&"意大利"!=i&&"西班牙"!=i&&"法国"!=i||a++;if(0!=a){var d=[];for(var o in t.leftNavData.Amazon){if("英国"==o||"德国"==o||"意大利"==o||"西班牙"==o||"法国"==o)for(var n=0;n<t.leftNavData.Amazon[o].length;n++)d.push(t.leftNavData.Amazon[o][n]);console.log(t.leftNavData.Amazon[o])}d=[].concat(s()(new l.a(d))),t.leftNavData.Amazon["欧洲"]=d,t.leftNavData.Amazon.英国&&delete t.leftNavData.Amazon.英国,t.leftNavData.Amazon.德国&&delete t.leftNavData.Amazon.德国,t.leftNavData.Amazon.意大利&&delete t.leftNavData.Amazon.意大利,t.leftNavData.Amazon.西班牙&&delete t.leftNavData.Amazon.西班牙,t.leftNavData.Amazon.法国&&delete t.leftNavData.Amazon.法国}})},mounted:function(){window.addEventListener("scroll",this.handleScroll)}},c={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{attrs:{id:"MerchandiseNews"}},[a("el-menu",{staticClass:"leftNav",attrs:{"default-active":"0-0-0","unique-opened":""}},t._l(t.leftNavData,function(e,i){return a("el-submenu",{key:i,attrs:{index:i+""}},[a("template",{slot:"title"},[t._v(t._s(i))]),t._v(" "),t._l(e,function(e,l){return a("el-submenu",{key:l,attrs:{index:l+""}},[a("template",{slot:"title"},[t._v(t._s(l))]),t._v(" "),t._l(e,function(e,d){return a("el-menu-item",{key:d,attrs:{index:l+e},on:{click:function(a){return t.NavClick(i,l,e)}}},[t._v(t._s(e))])})],2)})],2)}),1),t._v(" "),a("header",{staticStyle:{"font-size":"16px","line-height":"40px"}},[a("span",{staticStyle:{"padding-left":"20px"}},[t._v(t._s(t.firstData)+"-"+t._s(t.secondData)+"-"+t._s(t.threeData))]),t._v(" "),a("el-form",{attrs:{inline:!0}},[a("el-form-item",{attrs:{label:"产品编码"}},[a("el-select",{model:{value:t.dropProductCode,callback:function(e){t.dropProductCode=e},expression:"dropProductCode"}},t._l(t.productCodeList,function(t,e){return a("el-option",{key:e,attrs:{value:t.product_code,label:t.product_code}})}),1)],1),t._v(" "),a("el-form-item",{attrs:{label:"关键字"}},[a("el-input",{on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.search()}},model:{value:t.searchData,callback:function(e){t.searchData=e},expression:"searchData"}})],1),t._v(" "),a("el-form-item",[a("el-button",{staticClass:"searchBtn",attrs:{type:"primary"},on:{click:function(e){return t.search()}}},[t._v("查找")]),t._v(" "),a("el-button",{staticClass:"clearBtn",attrs:{type:"primary"},on:{click:t.clearSearchInfo}},[t._v("重置")])],1)],1)],1),t._v(" "),a("table",{staticClass:"MN_table",staticStyle:{"margin-left":"2vwl"}},[a("tr",{staticClass:"title"},[a("el-button",{staticClass:"Btn",attrs:{type:"primary",size:"small"},on:{click:function(e){return t.addNewdata()}}},[t._v("新增")]),t._v(" "),a("el-button",{staticClass:"Btn",attrs:{size:"small",type:"primary"},on:{click:function(e){return t.openedit()}}},[t._v("编辑")]),t._v(" "),a("el-button",{staticClass:"Btn",attrs:{type:"danger",size:"small"},on:{click:function(e){return t.deleteData()}}},[t._v("删除")]),t._v(" "),a("el-button",{staticClass:"Btn uploadExcel",attrs:{size:"small",type:"primary"}},[t._v("上传excel文件"),a("input",{ref:"uploadExcel",attrs:{type:"file",accept:"application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"},on:{change:t.changeFile}})]),t._v(" "),t._v("\n\n      商品信息\n    ")],1),t._v(" "),t._m(0),t._v(" "),a("tbody",t._l(t.tableList,function(e,i){return a("tr",{key:i,on:{click:function(e){return t.clickTr(e,i)}}},[a("td",[a("input",{staticClass:"checkLI",attrs:{type:"checkbox"},domProps:{value:e.id}})]),t._v(" "),a("td",[t._v(t._s(i+1+50*(t.page-1)))]),t._v(" "),a("td",[t._v(t._s(e.country))]),t._v(" "),a("td",[t._v(t._s(e.site))]),t._v(" "),a("td",[t._v(t._s(e.platform))]),t._v(" "),a("td",[t._v(t._s(e.product_code))]),t._v(" "),a("td",[t._v(t._s(e.spu))]),t._v(" "),a("td",[t._v(t._s(e.sku))]),t._v(" "),a("td",[t._v(t._s(e.product_name))]),t._v(" "),a("td",[t._v(t._s(e.product_type))]),t._v(" "),a("td",[t._v(t._s(e.commodity_state))]),t._v(" "),a("td",[t._v(t._s(e.commodity_price))]),t._v(" "),a("td",[t._v(t._s(e.asin))]),t._v(" "),a("td",[t._v(t._s(e.fnsku))]),t._v(" "),a("td",[t._v(t._s(e.upc))]),t._v(" "),a("td",[t._v(t._s(e.begin_sell_date))]),t._v(" "),a("td",[t._v(t._s(e.over_sell_date))]),t._v(" "),a("td",[e.check_time?a("span",{staticClass:"alink",staticStyle:{display:"block","text-decoration":"underline",color:"blue","z-index":"3",width:"100%",height:"100%",cursor:"pointer"}},[t._v(t._s(e.check_time))]):a("span",{staticStyle:{display:"block","text-decoration":"underline",color:"blue","z-index":"3",width:"100%",height:"100%",cursor:"pointer"}},[t._v("暂无记录")])]),t._v(" "),a("td",[t._v(t._s(e.product_link))])])}),0)]),t._v(" "),t.pageShow?a("el-pagination",{staticClass:"pagetotle",attrs:{background:"","current-page":t.page,layout:"total,prev, pager, next, jumper",total:t.total,"page-size":50},on:{"current-change":t.handleCurrentChange}}):t._e(),t._v(" "),a("el-dialog",{attrs:{title:"新增",visible:t.centerDialogVisible,"close-on-click-modal":!1,width:"55%",center:""},on:{"update:visible":function(e){t.centerDialogVisible=e}}},[a("el-form",{attrs:{inline:!0,"label-width":"100px"}},[a("el-form-item",{attrs:{label:"站点"}},[a("el-input",{attrs:{readonly:""},model:{value:t.addSite,callback:function(e){t.addSite=e},expression:"addSite"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"国家"}},[a("el-input",{attrs:{readonly:""},model:{value:t.addCountry,callback:function(e){t.addCountry=e},expression:"addCountry"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"平台"}},[a("el-input",{attrs:{readonly:""},model:{value:t.addplatform,callback:function(e){t.addplatform=e},expression:"addplatform"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"产品编码"}},[a("el-select",{model:{value:t.addProduct_code,callback:function(e){t.addProduct_code=e},expression:"addProduct_code"}},t._l(t.addProduct_codeList,function(t,e){return a("el-option",{key:e,attrs:{value:t.product_code,label:t.product_code}})}),1)],1),t._v(" "),a("el-form-item",{attrs:{label:"SPU"}},[a("el-input",{model:{value:t.addSpu,callback:function(e){t.addSpu=e},expression:"addSpu"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"SKU"}},[a("el-input",{model:{value:t.addSku,callback:function(e){t.addSku=e},expression:"addSku"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"状态"}},[a("el-select",{model:{value:t.addState,callback:function(e){t.addState=e},expression:"addState"}},t._l(t.stateList,function(t,e){return a("el-option",{key:e,attrs:{value:t.state,label:t.state}})}),1)],1),t._v(" "),a("el-form-item",{attrs:{label:"Asin"}},[a("el-input",{model:{value:t.addAsin,callback:function(e){t.addAsin=e},expression:"addAsin"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"Fnsku"}},[a("el-input",{model:{value:t.addFnsku,callback:function(e){t.addFnsku=e},expression:"addFnsku"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"UPC"}},[a("el-input",{model:{value:t.addUPC,callback:function(e){t.addUPC=e},expression:"addUPC"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"开始销售时间"}},[a("el-date-picker",{attrs:{"value-format":"yyyy-MM-dd",type:"date",placeholder:"选择日期"},model:{value:t.addStardate,callback:function(e){t.addStardate=e},expression:"addStardate"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"停止销售时间"}},[a("el-date-picker",{attrs:{"value-format":"yyyy-MM-dd",type:"date",placeholder:"选择日期"},model:{value:t.addenddate,callback:function(e){t.addenddate=e},expression:"addenddate"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"是否跟卖链接"}},[a("el-select",{on:{change:function(e){return t.addblo()}},model:{value:t.addsellFlag,callback:function(e){t.addsellFlag=e},expression:"addsellFlag"}},[a("el-option",{attrs:{value:"跟卖链接",label:"跟卖链接"}}),t._v(" "),a("el-option",{attrs:{value:"原链接",label:"原链接"}})],1)],1),t._v(" "),a("el-form-item",{directives:[{name:"show",rawName:"v-show",value:t.isShowSell,expression:"isShowSell"}],attrs:{label:"跟卖链接"}},[a("el-input",{model:{value:t.addsellLink,callback:function(e){t.addsellLink=e},expression:"addsellLink"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"产品链接"}},[a("el-input",{model:{value:t.addoriginalLink,callback:function(e){t.addoriginalLink=e},expression:"addoriginalLink"}})],1),t._v(" "),a("el-form-item",{staticClass:"lastBtnGroup"},[a("el-button",{attrs:{type:"primary"},on:{click:function(e){return t.addSubmit()}}},[t._v("保 存")]),t._v(" "),a("el-button",{attrs:{type:"warning"},on:{click:function(e){return t.addReset()}}},[t._v("重 置")])],1)],1)],1),t._v(" "),a("el-dialog",{attrs:{title:"编辑",visible:t.centerDialogVisible2,"close-on-click-modal":!1,width:"20%",center:""},on:{"update:visible":function(e){t.centerDialogVisible2=e}}},[a("el-form",{attrs:{inline:!0,"label-width":"100px"}},[a("el-form-item",{attrs:{label:"站点"}},[a("el-input",{attrs:{readonly:""},model:{value:t.editSite,callback:function(e){t.editSite=e},expression:"editSite"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"国家"}},[a("el-input",{attrs:{readonly:""},model:{value:t.editCountry,callback:function(e){t.editCountry=e},expression:"editCountry"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"平台"}},[a("el-input",{attrs:{readonly:""},model:{value:t.editplatform,callback:function(e){t.editplatform=e},expression:"editplatform"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"产品编码"}},[a("el-select",{model:{value:t.editProduct_code,callback:function(e){t.editProduct_code=e},expression:"editProduct_code"}},t._l(t.editProduct_codeList,function(t,e){return a("el-option",{key:e,attrs:{value:t.product_code,label:t.product_code}})}),1)],1),t._v(" "),a("el-form-item",{attrs:{label:"SPU"}},[a("el-input",{model:{value:t.editSpu,callback:function(e){t.editSpu=e},expression:"editSpu"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"SKU"}},[a("el-input",{model:{value:t.editSku,callback:function(e){t.editSku=e},expression:"editSku"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"状态"}},[a("el-select",{model:{value:t.editState,callback:function(e){t.editState=e},expression:"editState"}},t._l(t.stateList,function(t,e){return a("el-option",{key:e,attrs:{value:t.state,label:t.state}})}),1)],1),t._v(" "),a("el-form-item",{attrs:{label:"Asin"}},[a("el-input",{model:{value:t.editAsin,callback:function(e){t.editAsin=e},expression:"editAsin"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"Fnsku"}},[a("el-input",{model:{value:t.editFnsku,callback:function(e){t.editFnsku=e},expression:"editFnsku"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"UPC"}},[a("el-input",{model:{value:t.editUPC,callback:function(e){t.editUPC=e},expression:"editUPC"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"开始销售时间"}},[a("el-date-picker",{attrs:{"value-format":"yyyy-MM-dd",type:"date",placeholder:"选择日期"},model:{value:t.editStardate,callback:function(e){t.editStardate=e},expression:"editStardate"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"停止销售时间"}},[a("el-date-picker",{attrs:{"value-format":"yyyy-MM-dd",type:"date",placeholder:"选择日期"},model:{value:t.editenddate,callback:function(e){t.editenddate=e},expression:"editenddate"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"是否跟卖链接"}},[a("el-select",{on:{change:function(e){return t.editblo()}},model:{value:t.editsellFlag,callback:function(e){t.editsellFlag=e},expression:"editsellFlag"}},[a("el-option",{attrs:{value:"跟卖链接",label:"跟卖链接"}}),t._v(" "),a("el-option",{attrs:{value:"原链接",label:"原链接"}})],1)],1),t._v(" "),a("el-form-item",{directives:[{name:"show",rawName:"v-show",value:t.isShowSell1,expression:"isShowSell1"}],attrs:{label:"跟卖链接"}},[a("el-input",{model:{value:t.editsellLink,callback:function(e){t.editsellLink=e},expression:"editsellLink"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"产品链接"}},[a("el-input",{model:{value:t.editoriginalLink,callback:function(e){t.editoriginalLink=e},expression:"editoriginalLink"}})],1),t._v(" "),a("el-form-item",{staticClass:"lastBtnGroup"},[a("el-button",{attrs:{type:"primary",size:"small"},on:{click:function(e){return t.editSubmit()}}},[t._v("提 交")])],1)],1)],1)],1)},staticRenderFns:[function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("thead",[a("tr",[a("th"),t._v(" "),a("th",[t._v("序号")]),t._v(" "),a("th",[t._v("国家")]),t._v(" "),a("th",[t._v("站点")]),t._v(" "),a("th",[t._v("平台")]),t._v(" "),a("th",[t._v("产品编码")]),t._v(" "),a("th",[t._v("spu")]),t._v(" "),a("th",[t._v("sku")]),t._v(" "),a("th",[t._v("品名")]),t._v(" "),a("th",[t._v("类别")]),t._v(" "),a("th",[t._v("状态")]),t._v(" "),a("th",[t._v("价格")]),t._v(" "),a("th",[t._v("Asin")]),t._v(" "),a("th",[t._v("Fnsku")]),t._v(" "),a("th",[t._v("Upc")]),t._v(" "),a("th",[t._v("开始销售时间")]),t._v(" "),a("th",[t._v("停止销售时间")]),t._v(" "),a("th",[t._v("操作记录")]),t._v(" "),a("th",[t._v("产品链接")])])])}]};var u=a("VU/8")(r,c,!1,function(t){a("qpbd"),a("jBir"),a("sGl+")},"data-v-4b64aa3a",null);e.default=u.exports},jBir:function(t,e){},qpbd:function(t,e){},"sGl+":function(t,e){}});
//# sourceMappingURL=16.ba33049577e03550113c.js.map