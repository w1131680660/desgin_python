webpackJsonp([43],{Rvg7:function(e,t){},b4VU:function(e,t,i){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var a=i("mvHQ"),o=i.n(a),n=i("BO1k"),s=i.n(n),l=i("pFYg"),r=i.n(l),c={name:"",props:{},components:{},data:function(){return{curIndex:0,menuPlatFormList:[],menuCountryList:[],menuSiteList:[],showCountryList:[],showSiteList:[],lastSiteList:[],checkedPlatform:"",checkedCountry:"",checkedSite:"",checkedType:"钢木",stockCalculationList:[],editForm:{averageNum:"",saleDays:"",sku:"",buhuoNum:""},formRules:{averageNum:[{required:!0,message:"请输入均单量",trigger:"blur"}],buhuoNum:[{required:!0,message:"请输入补货数量",trigger:"blur"}],saleDays:[{required:!0,message:"请输入可售天数",trigger:"blur"}],containNum:[{required:!0,message:"请输入货柜号",trigger:"blur"}],stockType:[{required:!0,message:"请输入仓库类型",trigger:"blur"}],stockCode:[{required:!0,message:"请输入仓库编码",trigger:"blur"}],stockName:[{required:!0,message:"请输入仓库名称",trigger:"blur"}],mudigang:[{required:!0,message:"请输入目的港",trigger:"blur"}],fahuoDate:[{type:"string",required:!0,message:"请选择发货日期",trigger:"change"}],loadingDate:[{required:!0,message:"请输入装柜天数",trigger:"blur"}],shippingCycle:[{required:!0,message:"请输入海运周期",trigger:"blur"}]},isShowInput:[],editDayDialogVisible:!1,editDayForm:{loadingDate:"",shippingCycle:"",buhouDate:"",buhouDays:""},loadingDate:"",shippingCycle:"",buhouDate:"",buhouDays:"",isDateDisabled:!1,isDaysDisabled:!1,xiadanDialogVisible:!1,xiadanForm:{containNum:"",fahuoDate:"",stockType:"",stockCode:"",stockName:"",mudigang:""},stockTypeList:["FBA","海外仓"],loading:!0,currentPage:1,total:0,pageSize:50,monitorDialogVisible:!1,stockMonitorList:[],containerList:[],tableFinalList:["在途数量","库存合计","均单量","预计售空日期","提示"],tableLoading:!0,xiadanDisabled:!1}},computed:{seleteDate:function(){return this.editDayForm.buhouDate},seleteDays:function(){return this.editDayForm.buhouDays}},watch:{seleteDate:function(e){null===e&&(this.isDaysDisabled=!1)},seleteDays:function(e){null===e&&(this.isDateDisabled=!1)}},methods:{getMenuList:function(){var e=this;this.$api.getStockMenuList().then(function(t){console.log(t),e.menuPlatFormList=t.data.platform_list,e.menuCountryList=t.data.country_list,e.menuSiteList=t.data.site_list,e.showCountryList=e.menuCountryList[0],e.showSiteList=e.menuSiteList[0],e.lastSiteList=e.showSiteList[0],e.checkedPlatform=e.menuPlatFormList[0],e.checkedCountry=e.showCountryList[0],e.checkedSite=e.lastSiteList[0],e.thirdClick(e.checkedPlatform,e.checkedCountry,e.checkedSite),e.getDayInfo()})},getDayInfo:function(){var e=this;this.$api.getDay(this.checkedPlatform,this.checkedCountry,this.checkedSite,this.checkedType).then(function(t){console.log(t),e.loadingDate=t.data.data[0],e.shippingCycle=t.data.data[1],e.buhouDays=t.data.data[2],e.buhouDate=t.data.data[3]})},onceClick:function(e){this.showCountryList=[],this.showSiteList=[],this.showCountryList=this.menuCountryList[e],this.showSiteList=this.menuSiteList[e]},secondClick:function(e){this.lastSiteList=[],this.lastSiteList=this.showSiteList[e]},thirdClick:function(e,t,i){var a=this;this.stockCalculationList=[],this.checkedPlatform=e,this.checkedCountry=t,this.checkedSite=i,this.loading=!0,this.getDayInfo(),this.$api.stockCalculation(e,t,i,this.checkedType).then(function(e){console.log(e),a.stockCalculationList=a.$utils.deepClone(e.data.data),a.loading=!1;var t=[],i=a.stockCalculationList,o=function(e){if(1==i.slice(0,e).some(function(t){return t[0]==i[e][0]}))return"continue";var o={};o.spu=i[e][0],o.buhuo=[];var n=[];for(var l in i)if(i[e][0]===i[l][0]){var c={};c.index=l,c.num=i[l][6],o.buhuo.push(c),n.push(i[l][6])}t.push(o);var d=(n=a.$utils.quicksort(n))[0];console.log(o.buhuo,void 0===d?"undefined":r()(d));var u=function(e){if(e.num-d>=500&&"钢木"==a.checkedType||e.num-d>=200&&"魔片"==a.checkedType){var t=document.getElementsByClassName("el-table__row");a.$nextTick(function(){console.log("打印row",t,e,e.index,t[e.index]),t[e.index].style.color="red";var i=parseInt(e.index)+1,a=document.querySelectorAll(".el-table__body tr:nth-child("+i+") input"),o=!0,n=!1,l=void 0;try{for(var r,c=s()(a);!(o=(r=c.next()).done);o=!0){r.value.style.color="red"}}catch(e){n=!0,l=e}finally{try{!o&&c.return&&c.return()}finally{if(n)throw l}}console.log(a)})}},h=!0,m=!1,p=void 0;try{for(var y,f=s()(o.buhuo);!(h=(y=f.next()).done);h=!0){u(y.value)}}catch(e){m=!0,p=e}finally{try{!h&&f.return&&f.return()}finally{if(m)throw p}}};for(var n in i)o(n)})},typeClick:function(e){"钢木"===e?this.curIndex=0:"魔片"===e&&(this.curIndex=1),this.checkedType=e,this.getDayInfo(),this.thirdClick(this.checkedPlatform,this.checkedCountry,this.checkedSite)},getSummaries:function(e){var t=this,i=this.$createElement;console.log("计算");var a=e.columns,o=e.data,n=[];return a.forEach(function(e,s){if(0!==s){var l=o.map(function(t){return Number(t[e.property])});if(l.every(function(e){return isNaN(e)})||7!==s&&8!==s&&9!==s){if(s===a.length-1)return void(n[s]=i("el-button",{class:"disabled",attrs:{type:"primary",size:"mini",onclick:"goXiaDan()"}},["下单"]));n[s]=""}else n[s]=l.reduce(function(e,t){var i=Number(t);return isNaN(i)?Number(e):Number(e+t)},0),7===s&&(n[s]=Math.round(n[s])),8===s?n[s]=n[s].toFixed(2):9===s&&(n[s]=n[s].toFixed(3)),t.$nextTick(function(){n[8]>67?(document.querySelector(".el-table__footer-wrapper tbody tr td:nth-child(9)").style.background="red",document.querySelector(".disabled").style.display="none"):document.querySelector(".el-table__footer-wrapper tbody tr td:nth-child(9)").style.background="#F5F7FA";"美国"==t.checkedCountry&&n[9]>19500?(document.querySelector(".el-table__footer-wrapper tbody tr td:nth-child(10)").style.background="red",document.querySelector(".disabled").style.display="none"):document.querySelector(".el-table__footer-wrapper tbody tr td:nth-child(10)").style.background="#F5F7FA";(n[8]<67||67===n[8])&&(n[9]<19500||19500===n[9]||"美国"!==t.checkedCountry)&&(document.querySelector(".disabled").style.display="block")})}else n[s]="合计"}),n},dateEdit:function(){this.editDayForm.loadingDate=this.loadingDate,this.editDayForm.shippingCycle=this.shippingCycle,this.editDayForm.buhouDays=this.buhouDays,this.editDayDialogVisible=!0},editDayClose:function(){this.$refs.editDayRef.resetFields()},editDayConfirm:function(){var e=this;this.$refs.editDayRef.validate(function(t){if(t){var i=new FormData;i.append("platform",e.checkedPlatform),i.append("country",e.checkedCountry),i.append("site",e.checkedSite),i.append("delivery_day",e.editDayForm.loadingDate),i.append("shipping_cycle",e.editDayForm.shippingCycle),i.append("product_type",e.checkedType),i.append("replenish_can_sell_day_number",e.editDayForm.buhouDays),e.$api.editDay(i).then(function(t){console.log(t),e.$message.success("编辑成功"),e.getDayInfo(),e.editDayDialogVisible=!1})}})},handleOpen:function(e){},pickerChange:function(e){"日期"==e?this.isDaysDisabled=!0:this.isDateDisabled=!0},xiadan:function(){this.xiadanDialogVisible=!0},xiadanClose:function(){this.$refs.xiadanRef.resetFields()},xiadanConfirm:function(){var e=this;this.$refs.xiadanRef.validate(function(t){if(t){for(var i=e.stockCalculationList,a=[],n="",s="",l=0;l<i.length-1;l++)if(0!=i[l][6]){n=i[l][1],s=i[l][6];var r={};r.sku=n,r.num=s,a.push(r)}console.log(a);var c=new FormData;c.append("platform",e.checkedPlatform),c.append("country",e.checkedCountry),c.append("site",e.checkedSite),c.append("container",e.xiadanForm.containNum),c.append("receive_data",o()(a)),c.append("delivery_date",e.xiadanForm.fahuoDate),c.append("warehouse_type",e.xiadanForm.stockType),c.append("warehouse_code",e.xiadanForm.stockCode),c.append("warehouse_name",e.xiadanForm.stockName),c.append("destination_port",e.xiadanForm.mudigang),e.$api.xiadan(c).then(function(t){console.log(t),e.$message.success("下单成功"),e.xiadanDialogVisible=!1})}})},editChange:function(e){var t=this;console.log(e),this.editForm.averageNum=this.stockCalculationList[e][4],this.editForm.buhuoNum=this.stockCalculationList[e][6],this.editForm.sku=this.stockCalculationList[e][1],console.log(this.editForm);var i=new FormData;i.append("platform",this.checkedPlatform),i.append("country",this.checkedCountry),i.append("site",this.checkedSite),i.append("sku",this.editForm.sku),i.append("average_order",this.editForm.averageNum),i.append("replenish_num",this.editForm.buhuoNum),this.$api.editDay(i).then(function(e){console.log(e),t.$message.success("编辑成功"),t.loading=!0,t.thirdClick(t.checkedPlatform,t.checkedCountry,t.checkedSite)})},handleCurrentChange:function(e){console.log(e)},checkedStockMonitor:function(){var e=this;this.tableLoading=!0,this.$api.stockMonitor(this.checkedPlatform,this.checkedCountry,this.checkedSite,this.checkedType).then(function(t){console.log(t),e.tableLoading=!1,e.containerList=t.data.header,e.stockMonitorList=t.data.data}),this.monitorDialogVisible=!0}},created:function(){this.getMenuList(),window.goXiaDan=this.xiadan},mounted:function(){},updated:function(){}},d={render:function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{attrs:{id:"ipi-board"}},[i("div",{staticClass:"left"},[e._m(0),e._v(" "),i("div",{staticClass:"left-content"},[i("h3",[e._v("请选择店铺")]),e._v(" "),i("el-menu",{staticClass:"el-menu-vertical-demo",attrs:{"default-active":"0-0-0","unique-opened":""}},e._l(e.menuPlatFormList,function(t,a){return i("el-submenu",{key:a,attrs:{index:a+""}},[i("template",{slot:"title"},[i("span",{staticStyle:{display:"inline-block",width:"100%"},on:{click:function(t){return e.onceClick(a)}}},[e._v(e._s(t))])]),e._v(" "),e._l(e.showCountryList,function(o,n){return i("el-submenu",{key:n,attrs:{index:a+"-"+n}},[i("template",{slot:"title"},[i("span",{staticStyle:{display:"inline-block",width:"100%"},on:{click:function(t){return e.secondClick(n)}}},[e._v(e._s(o))])]),e._v(" "),e._l(e.lastSiteList,function(s,l){return i("el-menu-item",{key:l,attrs:{index:a+"-"+n+"-"+l},on:{click:function(i){return e.thirdClick(t,o,s)}}},[i("span",[e._v(e._s(s))])])})],2)})],2)}),1)],1)]),e._v(" "),i("div",{staticClass:"right"},[i("div",{staticClass:"table"},[i("div",{staticClass:"way-days"},[i("el-button",{style:{"background-color":0===e.curIndex?"#66b1ff":"",color:0===e.curIndex?"#fff":""},attrs:{size:"mini"},on:{click:function(t){return e.typeClick("钢木")}}},[e._v("钢木")]),e._v(" "),i("el-button",{style:{"background-color":1===e.curIndex?"#66b1ff":"",color:1===e.curIndex?"#fff":""},attrs:{size:"mini"},on:{click:function(t){return e.typeClick("魔片")}}},[e._v("魔片")]),e._v(" "),i("span",[e._v("装柜天数："+e._s(e.loadingDate))]),e._v(" "),i("span",[e._v("海运周期："+e._s(e.shippingCycle))]),e._v(" "),i("span",[e._v("补后可售天数："+e._s(e.buhouDays))]),e._v(" "),i("el-button",{attrs:{type:"primary",size:"mini"},on:{click:e.dateEdit}},[e._v("编辑")]),e._v(" "),i("el-button",{attrs:{size:"mini"},on:{click:e.checkedStockMonitor}},[e._v("查看库存监测")])],1),e._v(" "),i("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],ref:"stockTable",staticStyle:{width:"100%"},attrs:{data:e.stockCalculationList,border:"","max-height":"700","element-loading-text":"拼命加载中呀","element-loading-spinner":"el-icon-loading","show-summary":"","summary-method":e.getSummaries}},[i("el-table-column",{attrs:{type:"index",width:"60",label:"序号"}}),e._v(" "),i("af-table-column",{attrs:{prop:"0",label:"spu"}}),e._v(" "),i("af-table-column",{attrs:{prop:"1",label:"sku"}}),e._v(" "),i("el-table-column",{attrs:{prop:"2",label:"库存"}}),e._v(" "),i("el-table-column",{attrs:{prop:"3",label:"在途数量"}}),e._v(" "),i("el-table-column",{attrs:{prop:"4",label:"均单量"},scopedSlots:e._u([{key:"default",fn:function(t){return[i("input",{directives:[{name:"model",rawName:"v-model",value:t.row[4],expression:"scope.row[4]"}],attrs:{type:"number"},domProps:{value:t.row[4]},on:{change:function(i){return e.editChange(t.$index)},input:function(i){i.target.composing||e.$set(t.row,4,i.target.value)}}})]}}])}),e._v(" "),i("el-table-column",{attrs:{prop:"5",label:"预计售空日期"}}),e._v(" "),i("el-table-column",{attrs:{prop:"6",label:"建议补货数量"},scopedSlots:e._u([{key:"default",fn:function(t){return[i("input",{directives:[{name:"model",rawName:"v-model",value:t.row[6],expression:"scope.row[6]"}],attrs:{type:"number"},domProps:{value:t.row[6]},on:{change:function(i){return e.editChange(t.$index)},input:function(i){i.target.composing||e.$set(t.row,6,i.target.value)}}})]}}])}),e._v(" "),i("el-table-column",{attrs:{prop:"7",label:"总体积/立方"}}),e._v(" "),i("el-table-column",{attrs:{prop:"8",label:"总重量/kg"}}),e._v(" "),i("el-table-column",{attrs:{prop:"9",label:"预计补后可售日期"}})],1)],1)]),e._v(" "),i("el-dialog",{ref:"editDayRef",attrs:{visible:e.editDayDialogVisible,width:"30%",center:""},on:{"update:visible":function(t){e.editDayDialogVisible=t},close:e.editDayClose}},[i("el-form",{ref:"editDayRef",attrs:{model:e.editDayForm,rules:e.formRules,"label-width":"140px"}},[i("el-form-item",{attrs:{label:"装柜天数",prop:"loadingDate"}},[i("el-input",{model:{value:e.editDayForm.loadingDate,callback:function(t){e.$set(e.editDayForm,"loadingDate",t)},expression:"editDayForm.loadingDate"}})],1),e._v(" "),i("el-form-item",{attrs:{label:"海运周期",prop:"shippingCycle"}},[i("el-input",{model:{value:e.editDayForm.shippingCycle,callback:function(t){e.$set(e.editDayForm,"shippingCycle",t)},expression:"editDayForm.shippingCycle"}})],1),e._v(" "),i("el-form-item",{attrs:{label:"补后可售天数",prop:"buhouDays"}},[i("el-input",{attrs:{disabled:e.isDaysDisabled},on:{change:function(t){return e.pickerChange("天数")}},model:{value:e.editDayForm.buhouDays,callback:function(t){e.$set(e.editDayForm,"buhouDays",t)},expression:"editDayForm.buhouDays"}})],1)],1),e._v(" "),i("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[i("el-button",{on:{click:function(t){e.editDayDialogVisible=!1}}},[e._v("取 消")]),e._v(" "),i("el-button",{attrs:{type:"primary"},on:{click:e.editDayConfirm}},[e._v("修 改")])],1)],1),e._v(" "),i("el-dialog",{attrs:{visible:e.xiadanDialogVisible,width:"40%",center:"","close-on-click-modal":!1,"close-on-press-escape":!1},on:{"update:visible":function(t){e.xiadanDialogVisible=t},close:e.xiadanClose}},[i("el-form",{ref:"xiadanRef",attrs:{model:e.xiadanForm,rules:e.formRules,"label-width":"140px"}},[i("el-form-item",{attrs:{label:"货柜号",prop:"containNum"}},[i("el-input",{model:{value:e.xiadanForm.containNum,callback:function(t){e.$set(e.xiadanForm,"containNum",t)},expression:"xiadanForm.containNum"}})],1),e._v(" "),i("el-form-item",{attrs:{label:"预计发货日期",prop:"fahuoDate"}},[i("el-date-picker",{attrs:{type:"date",placeholder:"选择日期",format:"yyyy-MM-dd","value-format":"yyyy-MM-dd"},model:{value:e.xiadanForm.fahuoDate,callback:function(t){e.$set(e.xiadanForm,"fahuoDate",t)},expression:"xiadanForm.fahuoDate"}})],1),e._v(" "),i("el-form-item",{attrs:{label:"仓库类型",prop:"stockType"}},[i("el-select",{attrs:{clearable:"",placeholder:"请选择"},model:{value:e.xiadanForm.stockType,callback:function(t){e.$set(e.xiadanForm,"stockType",t)},expression:"xiadanForm.stockType"}},e._l(e.stockTypeList,function(e,t){return i("el-option",{key:t,attrs:{label:e,value:e}})}),1)],1),e._v(" "),i("el-form-item",{attrs:{label:"仓库名称",prop:"stockName"}},[i("el-input",{model:{value:e.xiadanForm.stockName,callback:function(t){e.$set(e.xiadanForm,"stockName",t)},expression:"xiadanForm.stockName"}})],1)],1),e._v(" "),i("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[i("el-button",{on:{click:function(t){e.xiadanDialogVisible=!1}}},[e._v("取 消")]),e._v(" "),i("el-button",{attrs:{type:"primary"},on:{click:e.xiadanConfirm}},[e._v("下 单")])],1)],1),e._v(" "),i("el-dialog",{attrs:{visible:e.monitorDialogVisible,width:"96%",center:""},on:{"update:visible":function(t){e.monitorDialogVisible=t}}},[i("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.tableLoading,expression:"tableLoading"}],staticStyle:{width:"100%"},attrs:{data:e.stockMonitorList,border:"","max-height":"700","element-loading-text":"拼命加载中","element-loading-spinner":"el-icon-loading","element-loading-background":"rgba(255, 255, 255, 0.8)"}},[i("af-table-column",{attrs:{prop:"0",width:"160",label:"spu",fixed:"left"}}),e._v(" "),i("af-table-column",{attrs:{prop:"1",width:"160",label:"sku",fixed:"left"}}),e._v(" "),i("el-table-column",{attrs:{prop:"2",label:"fba",fixed:"left"}}),e._v(" "),e._l(e.containerList,function(e,t){return i("el-table-column",{key:t,attrs:{prop:3+t+"",label:e}})}),e._v(" "),e._l(e.tableFinalList,function(t,a){return i("el-table-column",{key:a+"a",attrs:{prop:3+e.containerList.length+a+"",label:t,fixed:"right",width:"110"}})})],2)],1)],1)},staticRenderFns:[function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"title",staticStyle:{"text-align":"center"}},[t("h2",[this._v("库存测算")])])}]};var u=i("VU/8")(c,d,!1,function(e){i("Rvg7"),i("yDHE")},"data-v-2d87ea5e",null);t.default=u.exports},yDHE:function(e,t){}});
//# sourceMappingURL=43.cddb630fa7a08f38091e.js.map