webpackJsonp([65],{QMlC:function(t,e){},Uu0U:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i={data:function(){return{formData3:null}},props:["type"],methods:{changeFile3:function(){if("template"!==this.type){console.log(1);var t=this.$refs.input3.files[0];if(t.name)if("txt"!==t.name.split(".")[1])return this.$refs.input3.files=null,void alert("请上传txt文件");this.formData3=new FormData,this.formData3.append("files",t)}},submitUpload3:function(){if("template"!==this.type){console.log(1);this.$axios.post(this._url2+"server/order_management/germany_upload/",this.formData3).then(function(t){200===t.data.code?alert("所有订单创建成功"):alert("订单未创建成功")})}}}},n={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",{staticClass:"shunfeng"},[e("el-form",[e("el-form-item",{attrs:{label:"魔方云仓批量发货"}},[e("input",{ref:"input3",attrs:{type:"file",value:"文件上传",accept:".txt"},on:{change:this.changeFile3}}),this._v(" "),e("el-button",{staticStyle:{"margin-left":"10px"},attrs:{size:"small",type:"primary"},on:{click:this.submitUpload3}},[this._v("提交")])],1)],1)],1)},staticRenderFns:[]};var s=a("VU/8")(i,n,!1,function(t){a("QMlC")},null,null);e.default=s.exports}});
//# sourceMappingURL=65.9418277e290e210da9b0.js.map