webpackJsonp([84],{GFuy:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=n("Gu7T"),a=n.n(i),s={name:"",props:{},components:{},data:function(){return{menuPlatFormList:[],menuCountryList:[],menuSiteList:[],showCountryList:[],showSiteList:[],lastSiteList:[],checkedPlatform:"",checkedCountry:"",checkedSite:"",checkedStatus:"",questionList:[],currentPage:1,total:0,pageSize:50}},computed:{},watch:{},methods:{getMenuList:function(){var t=this;this.$api.getMenuList().then(function(e){t.menuPlatFormList=e.data.data1,t.menuCountryList=e.data.data2,t.menuSiteList=e.data.data3})},onceClick:function(t){this.showCountryList=[],this.showSiteList=[],this.showCountryList=this.menuCountryList[t],this.showSiteList=this.menuSiteList[t]},secondClick:function(t){this.lastSiteList=[],this.lastSiteList=this.showSiteList[t]},thirdClick:function(t,e,n){var i=this;this.checkedPlatform=t,this.checkedCountry=e,this.checkedSite=n,this.checkedStatus="";this.$api.queryQandA(t,e,n,1).then(function(t){console.log(t),i.questionList=t.data.data,i.questionList=i.questionListSort(i.questionList),i.total=t.data.all_number,i.$nextTick(function(){i.$refs.QATable.bodyWrapper.scrollTop=0}),i.currentPage=1})},questionListSort:function(t){for(var e=[],n=0;n<t.length;n++)"未处理"==t[n][10]&&(e.push(t[n]),t.splice(n,1),n--);return e.push.apply(e,a()(t)),e},selectChange:function(t){},handleBefore:function(){var t=this;this.checkedStatus="未处理";this.$api.queryQandA(this.checkedPlatform,this.checkedCountry,this.checkedSite,1,this.checkedStatus).then(function(e){t.questionList=e.data.data,t.$nextTick(function(){t.$refs.QATable.bodyWrapper.scrollTop=0}),t.currentPage=1,t.total=e.data.all_number})},handleAfter:function(){var t=this;this.checkedStatus="已处理";this.$api.queryQandA(this.checkedPlatform,this.checkedCountry,this.checkedSite,1,this.checkedStatus).then(function(e){t.questionList=e.data.data,t.$nextTick(function(){t.$refs.QATable.bodyWrapper.scrollTop=0}),t.currentPage=1,t.total=e.data.all_number})},handleAll:function(){var t=this;this.checkedStatus="",this.$api.queryQandA(this.checkedPlatform,this.checkedCountry,this.checkedSite,1).then(function(e){t.questionList=e.data.data,t.questionList=t.questionListSort(t.questionList),t.$nextTick(function(){t.$refs.QATable.bodyWrapper.scrollTop=0}),t.currentPage=1,t.total=e.data.all_number})},goHandle:function(t){var e=this;console.log(t),this.$confirm("确定回复吗？","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){e.$api.updateSatus(t).then(function(t){console.log(t),e.thirdClick(e.checkedPlatform,e.checkedCountry,e.checkedSite),e.$message.success("回复成功")})}).catch(function(){e.$message({type:"info",message:"已取消回复"})})},handleCurrentChange:function(t){var e=this;console.log(t),this.$api.queryQandA(this.checkedPlatform,this.checkedCountry,this.checkedSite,t,this.checkedStatus).then(function(t){e.questionList=t.data.data,e.total=t.data.all_number,e.$nextTick(function(){e.$refs.QATable.bodyWrapper.scrollTop=0})})}},created:function(){this.getMenuList(),this.thirdClick("","","")},mounted:function(){}},c={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{attrs:{id:"ipi-board"}},[n("div",{staticClass:"left"},[t._m(0),t._v(" "),n("div",{staticClass:"left-content"},[n("h3",[t._v("请选择店铺")]),t._v(" "),n("el-menu",{staticClass:"el-menu-vertical-demo",attrs:{"unique-opened":""}},t._l(t.menuPlatFormList,function(e,i){return n("el-submenu",{key:i,attrs:{index:i+""}},[n("template",{slot:"title"},[n("span",{staticStyle:{display:"inline-block",width:"100%"},on:{click:function(e){return t.onceClick(i)}}},[t._v(t._s(e))])]),t._v(" "),t._l(t.showCountryList,function(a,s){return n("el-submenu",{key:s,attrs:{index:i+"-"+s}},[n("template",{slot:"title"},[n("span",{staticStyle:{display:"inline-block",width:"100%"},on:{click:function(e){return t.secondClick(s)}}},[t._v(t._s(a))])]),t._v(" "),t._l(t.lastSiteList,function(c,o){return n("el-menu-item",{key:o,attrs:{index:i+"-"+s+"-"+o},on:{click:function(n){return t.thirdClick(e,a,c)}}},[n("span",[t._v(t._s(c))])])})],2)})],2)}),1)],1)]),t._v(" "),n("div",{staticClass:"right"},[n("div",{staticClass:"button"},[n("el-button",{attrs:{type:"primary",size:"mini"},on:{click:t.handleAll}},[t._v("全部")]),t._v(" "),n("el-button",{attrs:{type:"primary",size:"mini"},on:{click:t.handleBefore}},[t._v("未处理")]),t._v(" "),n("el-button",{attrs:{type:"primary",size:"mini"},on:{click:t.handleAfter}},[t._v("已处理")])],1),t._v(" "),n("div",{staticClass:"table"},[n("el-table",{ref:"QATable",staticStyle:{width:"100%"},attrs:{data:t.questionList,border:"","max-height":"750"}},[n("el-table-column",{attrs:{type:"index"}}),t._v(" "),n("el-table-column",{attrs:{prop:"2",label:"站点",width:"100"}}),t._v(" "),n("el-table-column",{attrs:{prop:"3",label:"国家",width:"100"}}),t._v(" "),n("el-table-column",{attrs:{prop:"4",label:"邮件标题"}}),t._v(" "),n("el-table-column",{attrs:{prop:"5",label:"发件时间",width:"250"}}),t._v(" "),n("el-table-column",{attrs:{prop:"6",label:"回复情况",width:"200"},scopedSlots:t._u([{key:"default",fn:function(e){return["已处理"==e.row[6]?n("span",[t._v("已回复")]):n("el-link",{attrs:{type:"danger"},on:{click:function(n){return t.goHandle(e.row[0])}}},[t._v("未处理")])]}}])}),t._v(" "),n("el-table-column",{attrs:{prop:"7",label:"回复人",width:"150"}}),t._v(" "),n("el-table-column",{attrs:{prop:"8",label:"回复时间",width:"200"}})],1),t._v(" "),n("el-pagination",{staticStyle:{"text-align":"center","margin-top":"5px"},attrs:{"current-page":t.currentPage,"page-size":t.pageSize,layout:"total,prev, pager, next, jumper",total:t.total},on:{"current-change":t.handleCurrentChange,"update:currentPage":function(e){t.currentPage=e},"update:current-page":function(e){t.currentPage=e}}})],1)])])},staticRenderFns:[function(){var t=this.$createElement,e=this._self._c||t;return e("div",{staticClass:"title",staticStyle:{"text-align":"center"}},[e("h2",[this._v("页面维护-Q&A")])])}]};var o=n("VU/8")(s,c,!1,function(t){n("PxrS")},"data-v-5d41df1d",null);e.default=o.exports},PxrS:function(t,e){}});
//# sourceMappingURL=84.f89172b8ed0f3e3f3d8e.js.map