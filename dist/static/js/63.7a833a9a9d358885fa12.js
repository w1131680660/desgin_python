webpackJsonp([63],{"1s7L":function(t,e){},"K+St":function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var s={name:"",props:{},data:function(){return{personnelAch:[]}},computed:{},watch:{},methods:{visitAch:function(){var t=this;this.$api2.visitAch().then(function(e){console.log(e),t.personnelAch=e.data.data})}},created:function(){console.log(this.$api2),this.visitAch()},mounted:function(){}},i={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"achievements"},[n("h2",[t._v("个人绩效")]),t._v(" "),n("div",{staticClass:"table_box"},[n("table",{staticClass:"table"},[t._m(0),t._v(" "),n("tbody",t._l(t.personnelAch,function(e,s){return n("tr",{key:s},[0==s?n("td",[t._v(t._s(e.personnel_name))]):n("td"),t._v(" "),n("td",[t._v(t._s(e.proportion))]),t._v(" "),n("td",[t._v(t._s(e.evaluate_date))]),t._v(" "),n("td",[t._v(t._s(e.evaluate))])])}),0)])]),t._v(" "),n("div",{staticStyle:{"padding-top":"48px"}},[n("span",[t._v("前往")]),t._v(" "),n("router-link",{attrs:{to:"/achievements_eval"}},[t._v("员工绩效评定")])],1)])},staticRenderFns:[function(){var t=this.$createElement,e=this._self._c||t;return e("thead",[e("tr",[e("th",[this._v("姓名")]),this._v(" "),e("th",[this._v("本月绩效比例")]),this._v(" "),e("th",[this._v("绩效评定时间")]),this._v(" "),e("th",[this._v("评价")])])])}]};var a=n("VU/8")(s,i,!1,function(t){n("1s7L")},"data-v-ee080170",null);e.default=a.exports}});
//# sourceMappingURL=63.7a833a9a9d358885fa12.js.map