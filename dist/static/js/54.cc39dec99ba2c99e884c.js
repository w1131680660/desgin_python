webpackJsonp([54],{"3TEb":function(t,e){},"5YLn":function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=a("mvHQ"),i=a.n(n),s={data:function(){return{searchNew:!0,loading:!1,currentPage:1,totalNum:0,searchlist:[],data1:[],productlist:[],realProductList:[],channels:[],stores:[],countrys:[],types:["钢木","魔片"],warehouses:["海外仓","FBA"],products:[],warehouses_list:[],hj:[],tableData:[],zonji:{},form:{platform:"all",store:"all",country:"all",type:"钢木",warehouse:"all",product:"all"}}},methods:{rowClick:function(t,e,a){if(t.index)for(var n=this.tableData.findIndex(function(e){return e.index===t.index}),i=this.tableData[n].sku_data.length,s=n+1;s<=n+i;s++)this.tableData[s].hide=!this.tableData[s].hide},tableRowStyle:function(t){var e=t.row;t.rowIndex;return{display:e.hide?"none":"table-row"}},changePage:function(t){this.currentPage=t,this.searchNew=!1,this.searchInfo()},changeOpt:function(t){var e=this,a=i()(this.realProductList),n=JSON.parse(a);if(e.products=n,e.form.product="all","country"===t)if("all"!==e.form.country){var s=e._url2+"server/personnel_management/get_sign_area/";this.$axios.get(s,{params:{country:e.form.country}}).then(function(t){e.stores=t.data.data})}else e.stores=[],e.form.store="all";else"site"===t&&"all"!==e.form.store&&(e.products=[],e.productlist.forEach(function(t){t.site,e.form.store===t.site&&e.form.country===t.country&&e.products.push(t.product_name)}))},getSearchParams:function(){var t=this,e=this._url2+"server/order_management/get_search/";this.$axios.get(e).then(function(e){t.productlist=e.data.product,t.productlist.forEach(function(e){var a=e.product_code+e.product_name;t.realProductList.push(a),t.products.push(a)})}).catch(function(t){});var a=this._url2+"server/personnel_management/get_sign_country/";this.$axios.get(a).then(function(e){t.channels.push(e.data.data1),t.countrys=e.data.data})},searchInfoBtn:function(){this.searchNew=!0,this.searchInfo()},searchInfo:function(){var t=this;this.searchNew&&(this.currentPage=1),this.loading=!0;var e=[];for(var a in this.form){var n=this.form[a];if(!(n.indexOf("all")>-1)){var s={};s.key=a,s.value=n,e.push(s)}}var l=this._url2+"server/order_management/on_way_container/";this.$axios.get(l,{params:{data:i()(e),page:this.currentPage}}).then(function(e){t.totalNum=e.data.total_num;var a=e.data.data;t.warehouses_list=a.header,t.InitData(a),t.loading=!1})},clickRow:function(t,e){if(t.index)for(var a=this.tableData.findIndex(function(e){return e.index===t.index}),n=this.tableData[a].sku_data.length,i=a+1;i<=a+n;i++)this.tableData[i].hide=!this.tableData[i].hide},getAllData:function(){var t=this;this.loading=!0;var e=this._url2+"server/order_management/on_way_container/";this.$axios.get(e).then(function(e){var a=e.data.data;t.warehouses_list=a.header,t.totalNum=e.data.total_num,t.InitData(a),t.loading=!1})},InitData:function(t){var e=this;this.hj=t.data,this.tableData=t.data.filter(function(t,e){return e>0}),this.tableData.forEach(function(t,a){t.index=a+1+50*(Number(e.currentPage)-1)});for(var a=function(t){console.log("表格长度",e.tableData.length);var a=e.tableData[t].sku_data||[];a.length&&a.forEach(function(a,n){var i={};for(var s in a)i[s]=a[s];i.hide=!0,console.log("插入的位置",n+t+1),e.tableData.splice(n+t+1,0,i)})},n=0;n<this.tableData.length;n++)a(n);if(1===this.currentPage){for(var n in this.tableData[0])this.zonji[n]="";this.zonji.product_code="总计",this.zonji.fba=this.hj[0].fba_all_num,this.zonji.fbm=this.hj[0].fbm_all_num,this.zonji.stock_num=this.hj[0].stock_all_num}this.tableData.unshift(this.zonji)},headerStyle:function(t){t.row,t.column;var e=t.rowIndex,a=t.columnIndex;if(0===e&&0==a)return"overflow:initial"},indexMethod:function(t){return 0==t&&(t=""),t}},created:function(){this.getSearchParams(),this.getAllData()}},l={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"InTransitManage"},[a("div",{staticClass:"leftMenu"},[a("el-form",{staticStyle:{width:"100%"},attrs:{model:t.form,"label-width":"60px"}},[a("el-form-item",{attrs:{label:"渠道"}},[a("el-select",{staticStyle:{width:"100%"},attrs:{filterable:"",placeholder:"请选择渠道"},model:{value:t.form.platform,callback:function(e){t.$set(t.form,"platform",e)},expression:"form.platform"}},[a("el-option",{attrs:{value:"all",label:"全部"}}),t._v(" "),t._l(t.channels,function(t,e){return a("el-option",{key:e,attrs:{label:t,value:t}})})],2)],1),t._v(" "),a("el-form-item",{attrs:{label:"国家"}},[a("el-select",{staticStyle:{width:"100%"},attrs:{filterable:"",placeholder:"请选择渠道"},on:{change:function(e){return t.changeOpt("country")}},model:{value:t.form.country,callback:function(e){t.$set(t.form,"country",e)},expression:"form.country"}},[a("el-option",{attrs:{value:"all",label:"全部"}}),t._v(" "),t._l(t.countrys,function(t,e){return a("el-option",{key:e,attrs:{label:t,value:t}})})],2)],1),t._v(" "),a("el-form-item",{attrs:{label:"站点"}},[a("el-select",{staticStyle:{width:"100%"},attrs:{filterable:"",placeholder:"请选择站点"},on:{change:function(e){return t.changeOpt("site")}},model:{value:t.form.store,callback:function(e){t.$set(t.form,"store",e)},expression:"form.store"}},[a("el-option",{attrs:{value:"all",label:"全部"}}),t._v(" "),t._l(t.stores,function(t,e){return a("el-option",{key:e,attrs:{label:t,value:t}})})],2)],1),t._v(" "),a("el-form-item",{attrs:{label:"类型"}},[a("el-select",{staticStyle:{width:"100%"},attrs:{filterable:""},model:{value:t.form.type,callback:function(e){t.$set(t.form,"type",e)},expression:"form.type"}},t._l(t.types,function(t,e){return a("el-option",{key:e,attrs:{label:t,value:t}})}),1)],1),t._v(" "),a("el-form-item",{attrs:{label:"仓库"}},[a("el-select",{staticStyle:{width:"100%"},attrs:{placeholder:"请选择仓库",filterable:""},model:{value:t.form.warehouse,callback:function(e){t.$set(t.form,"warehouse",e)},expression:"form.warehouse"}},[a("el-option",{attrs:{value:"all",label:"全部"}}),t._v(" "),t._l(t.warehouses,function(t,e){return a("el-option",{key:e,attrs:{label:t,value:t}})})],2)],1),t._v(" "),a("el-form-item",{attrs:{label:"产品"}},[a("el-select",{staticStyle:{width:"100%"},attrs:{placeholder:"请选择编码+产品",filterable:""},model:{value:t.form.commodity_name,callback:function(e){t.$set(t.form,"commodity_name",e)},expression:"form.commodity_name"}},[a("el-option",{attrs:{value:"all",label:"全部"}}),t._v(" "),t._l(t.products,function(t,e){return a("el-option",{key:e,attrs:{label:t,value:t}})})],2)],1),t._v(" "),a("el-form-item",[a("el-button",{attrs:{icon:"el-icon-search",type:"primary"},on:{click:t.searchInfoBtn}},[t._v("搜索")])],1)],1)],1),t._v(" "),a("div",{staticClass:"rightMenu",staticStyle:{position:"relative"}},[a("h2",[t._v("在途货柜盘点")]),t._v(" "),a("div",{staticStyle:{position:"relative"}},[a("div",{staticClass:"loadingMask",style:{visibility:t.loading?"visible":"hidden"}},[a("i",{staticClass:"el-icon-loading"}),a("span",[t._v("加载中...")])]),t._v(" "),a("div",{staticClass:"on_way_table"},[a("table",{staticClass:"IntainsitionTable"},[a("thead",[a("tr",{staticStyle:{position:"sticky"}},[a("th",{staticClass:"fixed-column",staticStyle:{"z-index":"16"}},[t._v("\n                序号\n              ")]),t._v(" "),t._m(0),t._v(" "),a("th",{staticClass:"fixed-column",staticStyle:{"z-index":"14"}},[t._v("\n                sku\n              ")]),t._v(" "),a("th",{staticClass:"fixed-column",staticStyle:{"z-index":"13"}},[t._v("\n                库存总计\n              ")]),t._v(" "),a("th",{staticClass:"fixed-column",staticStyle:{"z-index":"12"}},[t._v("\n                FBA合计\n              ")]),t._v(" "),a("th",{staticClass:"fixed-column",staticStyle:{"z-index":"11"}},[t._v("\n                FBM合计\n              ")]),t._v(" "),t._l(t.warehouses_list,function(e,n){return a("th",{key:n,staticClass:"fixed-column",staticStyle:{"z-index":"10"}},[t._v("\n                "+t._s(e)+"\n              ")])})],2)]),t._v(" "),a("tbody",t._l(t.tableData,function(e,n){return a("tr",{directives:[{name:"show",rawName:"v-show",value:!e.hide,expression:"!item.hide"}],key:n,on:{click:function(a){return t.clickRow(e,n)}}},[a("td",{staticClass:"fixed-column",staticStyle:{"z-index":"6"}},[t._v("\n                "+t._s(e.index)+"\n              ")]),t._v(" "),a("td",{staticClass:"fixed-column",staticStyle:{"z-index":"5"}},[t._v("\n                "+t._s(e.product_code)+"\n              ")]),t._v(" "),a("td",{staticClass:"fixed-column",staticStyle:{"z-index":"4"}},[t._v("\n                "+t._s(e.sku)+"\n              ")]),t._v(" "),a("td",{staticClass:"fixed-column",staticStyle:{"z-index":"3"}},[t._v("\n                "+t._s(e.stock_num)+"\n              ")]),t._v(" "),a("td",{staticClass:"fixed-column",staticStyle:{"z-index":"2"}},[t._v("\n                "+t._s(e.fba)+"\n              ")]),t._v(" "),a("td",{staticClass:"fixed-column",staticStyle:{"z-index":"1"}},[t._v("\n                "+t._s(e.fbm)+"\n              ")]),t._v(" "),t._l(t.warehouses_list,function(n,i){return a("td",{key:i},[t._v("\n                "+t._s(e[n])+"\n              ")])})],2)}),0)])])]),t._v(" "),t.totalNum>0?a("el-pagination",{attrs:{"current-page":t.currentPage,"page-size":50,layout:"total, prev, pager, next,jumper",total:t.totalNum},on:{"current-change":t.changePage,"update:currentPage":function(e){t.currentPage=e},"update:current-page":function(e){t.currentPage=e}}}):t._e()],1)])},staticRenderFns:[function(){var t=this.$createElement,e=this._self._c||t;return e("th",{staticClass:"t_head_td fixed-column",staticStyle:{"z-index":"15"}},[e("div",{staticClass:"t_head"},[e("span",{staticStyle:{position:"absolute",left:"20px",bottom:"0px"}},[this._v("产品")]),this._v(" "),e("span",{staticStyle:{background:"rgb(229, 229, 229)",width:"1px",height:"175px",position:"absolute",transform:"rotate(-72deg)",top:"-60px",left:"83px"}}),this._v(" "),e("span",{staticStyle:{position:"absolute",top:"0px",right:"12px"}},[this._v("货柜仓库")])])])}]};var r=a("VU/8")(s,l,!1,function(t){a("sSbh"),a("3TEb")},"data-v-106b4657",null);e.default=r.exports},sSbh:function(t,e){}});
//# sourceMappingURL=54.cc39dec99ba2c99e884c.js.map