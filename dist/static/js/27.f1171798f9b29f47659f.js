webpackJsonp([27],{bQYT:function(e,t){},vRFr:function(e,t){},vtnx:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var l=a("pFYg"),o=a.n(l),n=a("mvHQ"),s=a.n(n),r={data:function(){return{loading:!1,currentPage:1,totalNum:0,showCol:!0,channels:[],stores:[],countrys:[],selOpts:[],warehouses:["FBA"],productnames:[],skus:[],all_skus:[],warehouses_:["FBA"],productnames_:["all"],skus_:["all"],form:{channel:"all",site:"all",country:"all",product_name:["all"],sku:["all"],warehouses:["all"]},tableData:[]}},watch:{productnames_:{deep:!0,handler:function(e,t){var a=e.indexOf("all"),l=t.indexOf("all");-1!=a&&-1==l&&e.length>1||-1==a&&-1==l&&e.length===this.productnames.length?this.productnames_=["all"]:-1!=a&&-1!=l&&e.length>1&&this.productnames_.splice(e.indexOf("all"),1),this.form.product_name=this.productnames_}},skus_:{deep:!0,handler:function(e,t){var a=e.indexOf("all"),l=t.indexOf("all");-1!=a&&-1==l&&e.length>1||-1==a&&-1==l&&e.length===this.skus.length?this.skus_=["all"]:-1!=a&&-1!=l&&e.length>1&&this.skus_.splice(e.indexOf("all"),1),this.form.sku=this.skus_}}},methods:{searchInfoFun:function(){this.currentPage=1,this.searchInfo()},changeOpt:function(){var e=this;if("all"!==this.form.country){var t=this._url2+"server/personnel_management/get_sign_area/";this.$axios.get(t,{params:{country:this.form.country}}).then(function(t){e.stores=t.data.data})}else this.stores=[],this.form.site="all"},changeStore:function(e){},change:function(e){"总计"===e.label&&(this.showCol=!this.showCol)},getRelativeParams:function(e,t){var a=this;this.$axios.get(e,{params:t}).then(function(e){"platform"===t.name?(console.log(e),a.stores=e.data.data):"site"===t.name?a.countrys=e.data.data:"country"===t.name&&(a.skus=e.data.data)})},getSearchParams:function(){var e=this,t=this._url2+"server/databases/get_search/";this.$axios.get(t).then(function(t){console.log(t),e.productnames=t.data.product_name_list,e.skus=t.data.sku_list;var a=s()(e.skus);e.all_skus=JSON.parse(a)}).catch(function(e){});var a=this._url2+"server/personnel_management/get_sign_country/";this.$axios.get(a).then(function(t){e.channels.push(t.data.data1),e.countrys=e.changeCountry(t.data.data)})},changeCountry:function(){for(var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:[],t=!1,a=[],l=0;l<e.length;l++){var o=e[l];"法国"!==o&&"德国"!==o&&"意大利"!==o&&"西班牙"!==o?a.push(o):t=!0}return t&&a.push("欧洲"),a},searchInfo:function(){var e=this;this.loading=!0;var t=[];for(var a in console.log(this.form),this.form){console.log(a,this.form[a]);var l=this.form[a];if(!(l.indexOf("all")>-1||!l||"object"===(void 0===l?"undefined":o()(l))&&l.length<1)){var n={},r=void 0;l instanceof Array?(console.log("sku",l),-1===l.indexOf("all")&&(r=l.join())):r=l,"channel"===a?(n.key="platform",n.value=r):(n.key=a,n.value=r),t.push(n)}}console.log("请求参数",t);var i=this._url2+"server/databases/get_stock_data/";console.log(t),this.$axios.get(i,{params:{data:s()(t),page:this.currentPage}}).then(function(t){e.loading=!1,console.log(t),e.tableData=t.data.data,e.totalNum=t.data.total_num,e.$nextTick(function(){e.$refs.stockpageTable.bodyWrapper.scrollTop=0})})},getAllData:function(){var e=this;this.loading=!0;var t=this._url2+"server/databases/get_stock_data/";this.$axios.get(t).then(function(t){console.log(t),e.tableData=t.data.data,e.totalNum=t.data.total_num,e.loading=!1})},changePage:function(e){this.currentPage=e,this.searchInfo()},indexMethod:function(e){return e+1+50*(this.currentPage-1)}},created:function(){this.getSearchParams(),this.getAllData()}},i={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{attrs:{id:"stockpage"}},[a("div",{staticClass:"tac"},[a("el-form",{ref:"form",staticStyle:{width:"100%"},attrs:{inline:!0,model:e.form,"label-width":"40px"}},[a("el-form-item",{attrs:{label:"渠道"}},[a("el-select",{staticStyle:{width:"100%"},attrs:{filterable:"",placeholder:"请选择渠道"},model:{value:e.form.channel,callback:function(t){e.$set(e.form,"channel",t)},expression:"form.channel"}},[a("el-option",{attrs:{value:"all",label:"全部"}}),e._v(" "),e._l(e.channels,function(e,t){return a("el-option",{key:t,attrs:{label:e,value:e}})})],2)],1),e._v(" "),a("el-form-item",{attrs:{label:"国家"}},[a("el-select",{staticStyle:{width:"100%"},attrs:{filterable:"",placeholder:"请选择渠道"},on:{change:e.changeOpt},model:{value:e.form.country,callback:function(t){e.$set(e.form,"country",t)},expression:"form.country"}},[a("el-option",{attrs:{value:"all",label:"全部"}}),e._v(" "),e._l(e.countrys,function(e,t){return a("el-option",{key:t,attrs:{label:e,value:e}})})],2)],1),e._v(" "),a("el-form-item",{attrs:{label:"站点"}},[a("el-select",{staticStyle:{width:"100%"},attrs:{filterable:"",placeholder:"请选择站点"},model:{value:e.form.site,callback:function(t){e.$set(e.form,"site",t)},expression:"form.site"}},[a("el-option",{attrs:{value:"all",label:"全部"}}),e._v(" "),e._l(e.stores,function(e,t){return a("el-option",{key:t,attrs:{label:e,value:e}})})],2)],1),e._v(" "),a("el-form-item",{attrs:{label:"品名"}},[a("el-select",{staticStyle:{width:"100%"},attrs:{"collapse-tags":!0,filterable:"",multiple:"",placeholder:"请选择品名"},model:{value:e.productnames_,callback:function(t){e.productnames_=t},expression:"productnames_"}},[a("el-option",{attrs:{value:"all",label:"全部"}}),e._v(" "),e._l(e.productnames,function(e,t){return a("el-option",{key:t,attrs:{label:e,value:e}})})],2)],1),e._v(" "),a("el-form-item",{attrs:{label:"SKU"}},[a("el-select",{staticStyle:{width:"100%"},attrs:{"collapse-tags":!0,multiple:"",placeholder:"请选择SKU",filterable:""},model:{value:e.skus_,callback:function(t){e.skus_=t},expression:"skus_"}},[a("el-option",{attrs:{value:"all",label:"全部"}}),e._v(" "),e._l(e.skus,function(e,t){return a("el-option",{key:t,attrs:{label:e,value:e}})})],2)],1),e._v(" "),a("el-form-item",{attrs:{label:"仓库"}},[a("el-select",{staticStyle:{width:"100%"},attrs:{placeholder:"请选择仓库",filterable:""},model:{value:e.warehouses_,callback:function(t){e.warehouses_=t},expression:"warehouses_"}},e._l(e.warehouses,function(e,t){return a("el-option",{key:t,attrs:{label:e,value:e}})}),1)],1),e._v(" "),a("el-form-item",[a("el-button",{attrs:{icon:"el-icon-search",type:"primary"},on:{click:e.searchInfoFun}},[e._v("搜索")])],1)],1)],1),e._v(" "),a("div",{staticClass:"right_table"},[a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],ref:"stockpageTable",staticStyle:{width:"100%"},attrs:{"highlight-current-row":"","element-loading-text":"拼命加载中","element-loading-spinner":"el-icon-loading","element-loading-background":"rgba(0, 0, 0, 0.3)",data:e.tableData,"max-height":"700"},on:{"header-click":e.change}},[a("el-table-column",{attrs:{label:"每日库存盘点"}},[a("el-table-column",{attrs:{label:"序号",type:"index",index:e.indexMethod,width:"60"}}),e._v(" "),a("el-table-column",{attrs:{prop:"platform",label:"渠道"}}),e._v(" "),a("el-table-column",{attrs:{prop:"site",label:"站点",width:"60"}}),e._v(" "),a("el-table-column",{attrs:{prop:"country",label:"国家",width:"60"}}),e._v(" "),a("el-table-column",{attrs:{prop:"product_code",label:"产品编码",width:"120"}}),e._v(" "),a("el-table-column",{attrs:{prop:"product_name",label:"品名",width:"220"}}),e._v(" "),a("el-table-column",{attrs:{prop:"spu",label:"spu",width:"200"}}),e._v(" "),a("el-table-column",{attrs:{prop:"sku",label:"sku",width:"200"}}),e._v(" "),a("el-table-column",{attrs:{prop:"all_nums",label:"总计"}}),e._v(" "),e.showCol?a("el-table-column",{attrs:{prop:"on_warehouse_num",label:"在库合计"}}):e._e(),e._v(" "),e.showCol?a("el-table-column",{attrs:{prop:"fba",label:"FBA库存"}}):e._e(),e._v(" "),e.showCol?a("el-table-column",{attrs:{prop:"fbm",label:"FBM库存"}}):e._e(),e._v(" "),e.showCol?a("el-table-column",{attrs:{prop:"on_way_nums",label:"在途合计"}}):e._e(),e._v(" "),e.showCol?a("el-table-column",{attrs:{prop:"on_way_fba",label:"在途FBA"}}):e._e(),e._v(" "),e.showCol?a("el-table-column",{attrs:{prop:"on_way_fbm",label:"在途FBM"}}):e._e(),e._v(" "),a("el-table-column",{attrs:{prop:"avg",label:"十日均单"}}),e._v(" "),a("el-table-column",{attrs:{prop:"expect_turnover",label:"期望营业额"}}),e._v(" "),a("el-table-column",{attrs:{prop:"estimate_sell_out_days",label:"预计售空天数"}}),e._v(" "),a("el-table-column",{attrs:{prop:"estimate_sell_out_date",label:"预计售空日期",width:"100"}})],1)],1),e._v(" "),a("el-pagination",{attrs:{"current-page":e.currentPage,"page-size":50,layout:"total, prev, pager, next,jumper",total:e.totalNum},on:{"current-change":e.changePage,"update:currentPage":function(t){e.currentPage=t},"update:current-page":function(t){e.currentPage=t}}})],1)])},staticRenderFns:[]};var c=a("VU/8")(r,i,!1,function(e){a("bQYT"),a("vRFr")},"data-v-a45cddf4",null);t.default=c.exports}});
//# sourceMappingURL=27.f1171798f9b29f47659f.js.map