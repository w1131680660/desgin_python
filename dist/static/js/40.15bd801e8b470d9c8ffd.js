webpackJsonp([40],{"/dzo":function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n={data:function(){return{title:"",loading:!1,currentPage:1,totalNum:0,form:{platform:"all",site:"all",country:"all",date:"all"},channels:[],stores:[],countries:[],timeranges:[15,30,60,90,150,365],tableBody:[],data1:[],data2:[],data3:[]}},computed:{title_:function(){return this.title}},methods:{indexMethod:function(t){return t+1+50*(this.currentPage-1)},changePage:function(t){this.currentPage=t,this.search()},changeOpt:function(t){var e=this;if("country"===t&&(this.form.station="all",this.stores=[],"all"!==this.form.country)){this.$axios.get(this._url2+"server/personnel_management/get_sign_area/",{params:{country:this.form.country}}).then(function(t){e.stores=t.data.data})}},search:function(){var t=this;console.log("搜索");var e="";for(var a in this.form)"all"!==this.form[a]&&(e+=this.form[a]+"----");this.title=e.replace(/-+$/g,""),this.loading=!0;var n={};for(var r in this.form){var l=this.form[r];n[r]="all"!==l?l:""}n.page=this.currentPage,this.$axios.get(this._url2+"server/order_management/order_refund/",{params:n}).then(function(e){t.tableBody=e.data.re_data,t.totalNum=0,e.data.count_data.length>0&&e.data.count_data[0].count_data&&(t.totalNum=e.data.count_data[0].count_data),t.$nextTick(function(){t.$refs.orderreturnTable.bodyWrapper.scrollTop=0}),t.loading=!1})},getOption:function(){var t=this;this.$axios.get(this._url2+"server/personnel_management/get_sign_country/").then(function(e){t.channels.push(e.data.data1),t.form.platform=t.channels[0],t.countries=e.data.data,t.form.country=t.countries[0]}).then(function(e){t.$axios.get(t._url2+"server/personnel_management/get_sign_area/",{params:{country:t.form.country}}).then(function(e){t.stores=e.data.data,t.form.site=t.stores[0],t.form.date=t.timeranges[0],t.search()})})}},created:function(){this.getOption()}},r={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"order_refund_Rate"},[a("div",{staticClass:"left_menu"},[a("el-form",{staticClass:"demo-form-inline",attrs:{inline:!0,model:t.form}},[a("el-form-item",{attrs:{label:"渠道"}},[a("el-select",{model:{value:t.form.platform,callback:function(e){t.$set(t.form,"platform",e)},expression:"form.platform"}},[a("el-option",{attrs:{label:"全部",value:"all"}}),t._v(" "),t._l(t.channels,function(t,e){return a("el-option",{key:e,attrs:{label:t,value:t}})})],2)],1),t._v(" "),a("el-form-item",{attrs:{label:"国家"}},[a("el-select",{on:{change:function(e){return t.changeOpt("country")}},model:{value:t.form.country,callback:function(e){t.$set(t.form,"country",e)},expression:"form.country"}},[a("el-option",{attrs:{label:"全部",value:"all"}}),t._v(" "),t._l(t.countries,function(t,e){return a("el-option",{key:e,attrs:{label:t,value:t}})})],2)],1),t._v(" "),a("el-form-item",{attrs:{label:"站点"}},[a("el-select",{model:{value:t.form.site,callback:function(e){t.$set(t.form,"site",e)},expression:"form.site"}},[a("el-option",{attrs:{label:"全部",value:"all"}}),t._v(" "),t._l(t.stores,function(t,e){return a("el-option",{key:e,attrs:{label:t,value:t}})})],2)],1),t._v(" "),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:t.search}},[t._v("搜索")])],1)],1)],1),t._v(" "),a("div",{staticClass:"right"},[a("div",{staticClass:"topOpt"},[a("div",[a("label",[t._v("时间范围")]),t._v(" "),a("el-select",{on:{change:t.search},model:{value:t.form.date,callback:function(e){t.$set(t.form,"date",e)},expression:"form.date"}},[a("el-option",{attrs:{label:"全部",value:"all"}}),t._v(" "),t._l(t.timeranges,function(t,e){return a("el-option",{key:e,attrs:{label:t+"天内",value:t}})})],2)],1)]),t._v(" "),a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.loading,expression:"loading"}],ref:"orderreturnTable",staticStyle:{width:"100%"},attrs:{data:t.tableBody,"element-loading-text":"拼命加载中","element-loading-spinner":"el-icon-loading","element-loading-background":"rgba(0, 0, 0, 0.3)"}},[a("el-table-column",{attrs:{label:t.title_,width:"100%",align:"center"}},[a("el-table-column",{attrs:{label:"序号",type:"index",index:t.indexMethod,align:"center",width:"60"}}),t._v(" "),a("el-table-column",{attrs:{prop:"site",label:"站点",align:"center",width:"100"}}),t._v(" "),a("el-table-column",{attrs:{prop:"country",label:"国家",align:"center",width:"100"}}),t._v(" "),a("el-table-column",{attrs:{prop:"name_shop",label:"店铺",align:"center",width:"100"}}),t._v(" "),a("el-table-column",{attrs:{prop:"product_code",label:"产品编码",align:"center",width:"150"}}),t._v(" "),a("el-table-column",{attrs:{prop:"product_name",label:"品名",align:"center"}}),t._v(" "),a("el-table-column",{attrs:{prop:"sku",label:"sku",align:"center"}}),t._v(" "),a("el-table-column",{attrs:{prop:"return_sku",label:"退款订单量",align:"center",width:"100"}}),t._v(" "),a("el-table-column",{attrs:{prop:"ord_sku",label:"总订单量",align:"center",width:"100"}}),t._v(" "),a("el-table-column",{attrs:{label:"退款率",align:"center",width:"100"},scopedSlots:t._u([{key:"default",fn:function(e){return[e.row.return_sku&&e.row.ord_sku?a("span",[t._v("\n              "+t._s((Number(e.row.return_sku)/Number(e.row.ord_sku)*100).toFixed(2)+"%")+"\n            ")]):a("span",[t._v("\n              "+t._s(0)+"\n            ")])]}}])})],1)],1),t._v(" "),a("el-pagination",{attrs:{"current-page":t.currentPage,"page-size":50,layout:"total,prev, pager, next,jumper",total:t.totalNum},on:{"current-change":t.changePage,"update:currentPage":function(e){t.currentPage=e},"update:current-page":function(e){t.currentPage=e}}})],1)])},staticRenderFns:[]};var l=a("VU/8")(n,r,!1,function(t){a("ddyy"),a("TCxF")},"data-v-36013673",null);e.default=l.exports},TCxF:function(t,e){},ddyy:function(t,e){}});
//# sourceMappingURL=40.15bd801e8b470d9c8ffd.js.map