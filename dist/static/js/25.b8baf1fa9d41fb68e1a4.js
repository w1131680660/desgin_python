webpackJsonp([25],{"+ce8":function(e,a,l){"use strict";Object.defineProperty(a,"__esModule",{value:!0});var t={data:function(){return{loading:!1,theadData:[{title:"中睿汇总",abbrName:[{prop:"zr_yye",label:"营业额合计"},{prop:"tb",label:"同比"},{prop:"zr_gghj",label:"广告合计"},{prop:"zr_ggzb",label:"广告占比"}]},{title:"胤佑美国",abbrName:[{prop:"yyus_yye",label:"营业额"},{prop:"yyus_gghf",label:"广告花费"},{prop:"yyus_ggzb",label:"广告占比"}]},{title:"爱瑙美国",abbrName:[{prop:"anus_yye",label:"营业额"},{prop:"anus_gghf",label:"广告花费"},{prop:"anus_ggzb",label:"广告占比"}]},{title:"利百锐美国",abbrName:[{prop:"lbrus_yye",label:"营业额"},{prop:"lbrus_gghf",label:"广告花费"},{prop:"lbrus_ggzb",label:"广告占比"}]},{title:"胤佑加拿大",abbrName:[{prop:"yyca_yye",label:"营业额"},{prop:"yyca_gghf",label:"广告花费"},{prop:"yyca_ggzb",label:"广告占比"}]},{title:"爱瑙加拿大",abbrName:[{prop:"anca_yye",label:"营业额"},{prop:"anca_gghf",label:"广告花费"},{prop:"anca_ggzb",label:"广告占比"}]},{title:"中睿欧洲",abbrName:[{prop:"zreu_yye",label:"营业额"},{prop:"zreu_gghf",label:"广告花费"},{prop:"zreu_ggzb",label:"广告占比"}]},{title:"京汇欧洲",abbrName:[{prop:"jheu_yye",label:"营业额"},{prop:"jheu_gghf",label:"广告花费"},{prop:"jheu_ggzb",label:"广告占比"}]},{title:"爱瑙欧洲",abbrName:[{prop:"aneu_yye",label:"营业额"},{prop:"aneu_gghf",label:"广告花费"},{prop:"aneu_ggzb",label:"广告占比"}]},{title:"中睿英国",abbrName:[{prop:"zruk_yye",label:"营业额"},{prop:"zruk_gghf",label:"广告花费"},{prop:"zruk_ggzb",label:"广告占比"}]},{title:"京汇英国",abbrName:[{prop:"jhuk_yye",label:"营业额"},{prop:"jhuk_gghf",label:"广告花费"},{prop:"jhuk_ggzb",label:"广告占比"}]},{title:"爱瑙英国",abbrName:[{prop:"anuk_yye",label:"营业额"},{prop:"anuk_gghf",label:"广告花费"},{prop:"anuk_ggzb",label:"广告占比"}]},{title:"胤佑日本",abbrName:[{prop:"yyjp_yye",label:"营业额"},{prop:"yyjp_gghf",label:"广告花费"},{prop:"yyjp_ggzb",label:"广告占比"}]},{title:"利百锐日本",abbrName:[{prop:"lbrjp_yye",label:"营业额"},{prop:"lbrjp_gghf",label:"广告花费"},{prop:"lbrjp_ggzb",label:"广告占比"}]},{title:"胤佑澳洲",abbrName:[{prop:"yyau_yye",label:"营业额"},{prop:"yyau_gghf",label:"广告花费"},{prop:"yyau_ggzb",label:"广告占比"}]},{title:"胤佑墨西哥",abbrName:[{prop:"yymx_yye",label:"营业额"},{prop:"yymx_gghf",label:"广告花费"},{prop:"yymx_ggzb",label:"广告占比"}]}],tableData:[],zr:[],zr2:[],form:{channel:"",monthPick:""},channels:["Amazon"],month_pickerOptions:{disabledDate:function(e){return e.getTime()>(new Date).getTime()}}}},created:function(){var e=this;this.$axios({url:this._url2+"server/stock_management/is_open/",method:"get"}).then(function(a){if(200==a.data.code){var l=new Date;l=l.getFullYear()+"-"+(l.getMonth()+1),e.getDailyData(l)}else alert("您没有权限进入这个页面"),e.$router.push("/Login")})},methods:{cellStyle:function(e){e.row;var a=e.column;e.rowIndex,e.columnIndex;if(a.label.includes("营业额"))return{background:"#ddd"}},queryData:function(){this.form.channel&&this.form.monthPick?(console.log(this.form),this.getDailyData(this.form.monthPick)):alert("请选择渠道和日期进行查询！")},change:function(){},getDailyData:function(e){var a=this;this.loading=!0,this.$axios.get(this._url2+"server/databases/get_everyday_report/",{params:{date:e}}).then(function(e){a.zr=e.data.data.zr,a.zr2=e.data.data.zr2,a.tableData=a.zr.concat(a.zr2),a.loading=!1})}}},r={render:function(){var e=this,a=e.$createElement,l=e._self._c||a;return l("div",{attrs:{id:"daily_operation_report1"}},[l("h2",[e._v("每日运营数据")]),e._v(" "),l("div",{staticClass:"dailyoperating"},[l("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],staticStyle:{width:"100%"},attrs:{"highlight-current-row":"","cell-style":e.cellStyle,data:e.tableData,"element-loading-text":"拼命加载中","element-loading-spinner":"el-icon-loading","element-loading-background":"rgba(0, 0, 0, 0.3)","max-height":"800"}},[l("el-table-column",{attrs:{fixed:"",width:"100"}},[l("el-table-column",{attrs:{prop:"date",label:"日期",width:"100"}})],1),e._v(" "),e._l(e.theadData,function(a,t){return l("el-table-column",{key:t,attrs:{label:a.title}},e._l(a.abbrName,function(e,a){return l("el-table-column",{key:a,attrs:{prop:e.prop,label:e.label,width:"80"}})}),1)})],2)],1)])},staticRenderFns:[]};var b=l("VU/8")(t,r,!1,function(e){l("LReg"),l("xjIV")},"data-v-e2e3ef82",null);a.default=b.exports},LReg:function(e,a){},xjIV:function(e,a){}});
//# sourceMappingURL=25.b8baf1fa9d41fb68e1a4.js.map