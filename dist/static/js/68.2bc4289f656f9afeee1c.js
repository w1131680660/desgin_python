webpackJsonp([68],{"+Irh":function(t,e){},TbgM:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=a("mtWM"),r=a.n(n),o={data:function(){return{beginTime:"",endTime:"",country:"",factory:"",tableList:[],total:0,page:1,countryList:[],factoryList:[]}},methods:{checkEmial:function(){var t=this;r()({url:this._url2+"server/customer_management/factory_feedback/",method:"get",params:{country:this.country,page:1,begin_time:this.beginTime,over_time:this.endTime,factory:this.factory}}).then(function(e){200==e.data.code&&(console.log(e),t.tableList=e.data.data,t.$nextTick(function(){$(".emailFeedback>tbody").scrollTop(0)}),t.total=e.data.count[0].count/5,t.page=1)})},getfilename:function(t){var e=t.lastIndexOf("/");return t.substring(e+1)},handleCurrentChange:function(t){var e=this;this.page=t,r()({url:this._url2+"server/customer_management/factory_feedback/",method:"get",params:{country:this.country,page:this.page,begin_time:this.beginTime,over_time:this.endTime,factory:this.factory}}).then(function(t){200==t.data.code&&(console.log(t),e.tableList=t.data.data,e.$nextTick(function(){$(".emailFeedback>tbody").scrollTop(0)}),e.total=t.data.count[0].count/5)})}},created:function(){var t=this;r()({url:this._url2+"server/customer_management/factory_feedback/",method:"get",params:{page:1}}).then(function(e){200==e.data.code&&(console.log(e),t.tableList=e.data.data,t.total=e.data.count[0].count/5,t.factoryList=e.data.factory_data)}),r()({url:this._url2+"server/personnel_management/get_sign_country/",method:"get"}).then(function(e){t.countryList=e.data.data})}},i={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("div",{staticClass:"nav",staticStyle:{background:"rgba(255, 255, 255, 0.9)"}},[a("div",[t._v("\n      国家:"),a("br"),t._v(" "),a("select",{directives:[{name:"model",rawName:"v-model",value:t.country,expression:"country"}],attrs:{name:"",id:""},on:{change:[function(e){var a=Array.prototype.filter.call(e.target.options,function(t){return t.selected}).map(function(t){return"_value"in t?t._value:t.value});t.country=e.target.multiple?a:a[0]},t.checkEmial]}},t._l(t.countryList,function(e,n){return a("option",{key:n,domProps:{value:e}},[t._v("\n          "+t._s(e)+"\n        ")])}),0)]),t._v(" "),a("div",[t._v("\n      工厂:"),a("br"),t._v(" "),a("select",{directives:[{name:"model",rawName:"v-model",value:t.factory,expression:"factory"}],attrs:{name:"",id:""},on:{change:[function(e){var a=Array.prototype.filter.call(e.target.options,function(t){return t.selected}).map(function(t){return"_value"in t?t._value:t.value});t.factory=e.target.multiple?a:a[0]},t.checkEmial]}},t._l(t.factoryList,function(e,n){return a("option",{key:n,domProps:{value:e.factory}},[t._v("\n          "+t._s(e.factory)+"\n        ")])}),0)]),t._v(" "),a("div",[t._v("\n      起始时间:\n      "),a("input",{directives:[{name:"model",rawName:"v-model",value:t.beginTime,expression:"beginTime"}],attrs:{type:"date",name:"",id:""},domProps:{value:t.beginTime},on:{change:t.checkEmial,input:function(e){e.target.composing||(t.beginTime=e.target.value)}}})]),t._v(" "),a("div",[t._v("\n      结束时间：\n      "),a("input",{directives:[{name:"model",rawName:"v-model",value:t.endTime,expression:"endTime"}],attrs:{type:"date"},domProps:{value:t.endTime},on:{change:t.checkEmial,input:function(e){e.target.composing||(t.endTime=e.target.value)}}})])]),t._v(" "),a("div",{staticClass:"main",staticStyle:{"margin-left":"13vw"}},[a("table",{staticClass:"emailFeedback"},[t._m(0),t._v(" "),a("tbody",t._l(t.tableList,function(e,n){return a("tr",{key:n},[a("td",[t._v(t._s(n+1+50*(t.page-1)))]),t._v(" "),a("td",[t._v(t._s(e.commodity_name))]),t._v(" "),a("td",[t._v(t._s(e.sku))]),t._v(" "),a("td",[t._v(t._s(e.country))]),t._v(" "),a("td",[t._v(t._s(e.order_number))]),t._v(" "),a("td",[t._v(t._s(e.container_num))]),t._v(" "),a("td",[t._v(t._s(e.factory))]),t._v(" "),a("td",[t._v(t._s(e.problem_type))]),t._v(" "),a("td",[a("div",{staticClass:"tdDiv"},[t._v(t._s(e.problem_content))])]),t._v(" "),a("td",[a("a",{attrs:{href:e.attachment_address,download:""}},[t._v(t._s(t.getfilename(e.attachment_address)))])]),t._v(" "),a("td",[t._v(t._s(e.upload_time))])])}),0)]),t._v(" "),a("el-pagination",{staticClass:"pagetotle",staticStyle:{margin:"1vh 0 0 38vw"},attrs:{background:"","current-page":t.page,layout:"prev, pager, next, jumper",total:t.total},on:{"current-change":t.handleCurrentChange}})],1)])},staticRenderFns:[function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("thead",[a("tr",[a("th",[t._v("序号")]),t._v(" "),a("th",[t._v("品名")]),t._v(" "),a("th",[t._v("SKU")]),t._v(" "),a("th",[t._v("国家")]),t._v(" "),a("th",[t._v("订单号")]),t._v(" "),a("th",[t._v("货柜号")]),t._v(" "),a("th",[t._v("工厂")]),t._v(" "),a("th",[t._v("问题类型")]),t._v(" "),a("th",[t._v("缺件\\破损情况")]),t._v(" "),a("th",[t._v("附件预览")]),t._v(" "),a("th",[t._v("提交时间")])])])}]};var c=a("VU/8")(o,i,!1,function(t){a("+Irh")},"data-v-d3101630",null);e.default=c.exports}});
//# sourceMappingURL=68.2bc4289f656f9afeee1c.js.map