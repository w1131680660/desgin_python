webpackJsonp([36],{"+LnQ":function(t,e){},kGYs:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=a("mtWM"),d=a.n(i),o={data:function(){return{pageShow:!0,pageFlag:!1,centerDialogVisible:!1,centerDialogVisible2:!1,tableList:[],channelList:[],productTypeList:[],productStateList:[],addProductId:"",addProductName:"",addProductType:"",addProductPackSize1:"",addProductPackSize2:"",addProductPackSize3:"",addProductSize1:"",addProductSize2:"",addProductSize3:"",productWeight:"",addState:"",editProductId:"",editProductName:"",editProductType:"",editProductPackSize1:"",editProductPackSize2:"",editProductPackSize3:"",editProductSize1:"",editProductSize2:"",editProductSize3:"",editproductWeight:"",editState:"",total:0,page:1,searchData:"",currentSelect:""}},methods:{changeSelect:function(t){console.log("切换input");document.querySelectorAll(".allcheck");this.currentSelect&&(this.currentSelect.checked=!1),this.currentSelect!==t.target?(t.target.checked=!0,this.currentSelect=t.target):this.currentSelect=""},getTableList:function(t){var e=this;if(t&&"新增"===t){var a=Math.ceil((this.total+1)/50);console.log("是不是同一页",Math.ceil(this.total/50),a,Math.ceil(this.total/50)!==a),Math.ceil(this.total/50)!==a&&(this.pageShow=!1,this.pageFlag=!0),this.page=a}if(t&&"删除"===t){var i=this.total-1;console.log("删除后条数",i),console.log("总条数",this.total),i<50*this.page&&(this.page=Math.ceil(i/50))}d()({url:this._url2+"server/databases/product_information",methods:"get",params:{page:this.page}}).then(function(t){e.tableList=t.data.data,console.log(t,55),e.channelList=t.data.platform_data,e.productTypeList=t.data.product_type_data,e.productStateList=t.data.product_state_data,e.total=t.data.count_data[0].count_id,e.$nextTick(function(){e.pageFlag&&(e.pageShow=!0)})})},openAdd:function(){this.centerDialogVisible2=!0,this.addProductId="",this.addProductName="",this.addProductType="",this.addProductSize1="",this.addProductSize2="",this.addProductSize3="",this.addProductPackSize1="",this.addProductPackSize2="",this.addProductPackSize3="",this.addState="",this.productWeight=""},addReset:function(){this.addProductId="",this.addProductName="",this.addProductType="",this.addProductSize1="",this.addProductSize2="",this.addProductSize3="",this.addProductPackSize1="",this.addProductPackSize2="",this.addProductPackSize3="",this.addState="",this.productWeight=""},isNum:function(t){return/^(\d+|\d+\.\d+)$/g.test(t)},addSubmit:function(){for(var t=this,e=1;e<=3;e++){var a="addProductSize"+e,i="addProductPackSize"+e;if(console.log("产品尺寸",this.isNum(this[a])),console.log("包装尺寸",this.isNum(this[i])),this[a]&&!this.isNum(this[a])||this[i]&&!this.isNum(this[i])||this.productWeight&&!this.isNum(this.productWeight))return void alert("产品尺寸/包装尺寸/重量请输入数字！")}if(""==this.addProductId||""==this.addProductName||""==this.addProductType||""==this.addState)alert("请填写产品编码，品名，类别，状态");else{var d=this.addProductSize1+"*"+this.addProductSize2+"*"+this.addProductSize3,o=this.addProductPackSize1+"*"+this.addProductPackSize2+"*"+this.addProductPackSize3,c=new FormData;console.log(d),console.log(o),c.append("product_code",this.addProductId),c.append("product_name",this.addProductName),c.append("product_type",this.addProductType),c.append("platform",this.addChannel),c.append("product_size",d),c.append("product_package_size",o),c.append("product_weight",this.productWeight),c.append("product_state",this.addState),c.append("platform",""),this.$axios.post(this._url2+"server/databases/product_information",c).then(function(e){200==e.data.code?(t.centerDialogVisible2=!1,alert("新增成功"),t.getTableList("新增")):500==e.data.code&&alert(e.data.msg)})}},deletProduct:function(){for(var t=this,e=document.querySelectorAll(".allcheck"),a=[],i=0;i<e.length;i++)1==e[i].checked&&a.push(e[i].value);a.length<1?alert("请选择您想要的数据删除"):this.$confirm("此操作将永久删除选中商品, 是否继续?","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){t.$axios.delete(t._url2+"server/databases/product_information",{params:{id:a}}).then(function(e){200==e.data.code&&(t.$message({type:"success",message:"删除成功!"}),t.getTableList("删除"))})}).catch(function(){})},openEdit:function(){for(var t=0,e=document.querySelectorAll(".allcheck"),a=0;a<e.length;a++)1==e[a].checked&&t++;if(1==t){this.centerDialogVisible=!0,console.log(this.tableList);for(var i=0;i<e.length;i++)if(1==e[i].checked)for(var d=0;d<this.tableList.length;d++)if(e[i].value==this.tableList[d].id){if(this.editProductName=this.tableList[d].product_name,this.editProductId=this.tableList[d].product_code,this.editproductWeight=this.tableList[d].product_weight,this.tableList[d].product_size){var o=this.tableList[d].product_size.split("*");this.editProductSize1=o[0],this.editProductSize2=o[1],this.editProductSize3=o[2]}if(this.tableList[d].product_package_size){var c=this.tableList[d].product_package_size.split("*");this.editProductPackSize1=c[0],this.editProductPackSize2=c[1],this.editProductPackSize3=c[2]}this.editProductType=this.tableList[d].product_type,this.editState=this.tableList[d].product_state}}else alert("请只选择一条数据编辑")},editReset:function(){this.editProductSize1="",this.editProductSize2="",this.editProductSize3="",this.editProductPackSize1="",this.editProductPackSize2="",this.editProductPackSize3="",this.editState="",this.editproductWeight=""},editSubmit:function(){var t=this;if(""==this.editState)alert("请填写状态");else{for(var e=document.querySelectorAll(".allcheck"),a="",i=0;i<e.length;i++)1==e[i].checked&&(a=e[i].value);var d=new FormData,o=this.editProductSize1+"*"+this.editProductSize2+"*"+this.editProductSize3,c=this.editProductPackSize1+"*"+this.editProductPackSize2+"*"+this.editProductPackSize3;d.append("id",a),console.log(a),d.append("product_code",this.editProductId),d.append("product_name",this.editProductName),d.append("product_type",this.editProductType),d.append("platform",this.editChannel),d.append("product_size",o),d.append("product_package_size",c),d.append("product_weight",this.editproductWeight),d.append("product_state",this.editState),this.$axios.put(this._url2+"server/databases/product_information",d).then(function(e){200==e.data.code&&(alert("修改成功"),t.getTableList())}),this.centerDialogVisible=!1}},search:function(){var t=this,e={condition:this.searchData,page:1};d()({url:this._url2+"server/databases/product_information",methods:"get",params:e}).then(function(e){console.log(e),t.tableList=e.data.data,t.total=e.data.count_data[0].count_id,t.page=1;for(var a=document.querySelectorAll(".allcheck"),i=0;i<a.length;i++)a[i].checked=!1})},goProductInformationDetails:function(t,e){t.target.constructor===HTMLTableCellElement&&(this.$store.commit("getIpQuery",{condition:this.searchData,page:this.page}),this.$router.push({path:"productInformationDetails",query:{id:e}}))},handleCurrentChange:function(t){var e=this;this.page=t;var a={condition:this.searchData,page:this.page};d()({url:this._url2+"server/databases/product_information",methods:"get",params:a}).then(function(t){console.log("切换页数",t),console.log(e.productStateList),e.tableList=t.data.data,e.total=t.data.count_data[0].count_id,e.productStateList=t.data.product_state_data||[],e.productTypeList=t.data.product_type_data||[],e.$nextTick(function(){$(".PI_table >tbody").scrollTop(0)})});for(var i=document.querySelectorAll(".allcheck"),o=0;o<i.length;o++)i[o].checked=!1}},created:function(){console.log(this.$store.state);var t=this.$store.state.PI_Query;if(console.log(t),t&&""!==t.page){var e=t;this.searchData=e.condition,this.handleCurrentChange(e.page)}else this.getTableList()}},c={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{attrs:{id:"productInformation"}},[a("header",[a("div",{staticStyle:{"font-size":"16px"}},[t._v("\n      搜索一下："),a("input",{directives:[{name:"model",rawName:"v-model",value:t.searchData,expression:"searchData"}],staticStyle:{height:"30px",padding:"0px 10px","border-radius":"4px",border:"1px solid #e5e5e5"},attrs:{type:"text"},domProps:{value:t.searchData},on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.search(e)},input:function(e){e.target.composing||(t.searchData=e.target.value)}}})]),t._v(" "),a("div",[a("el-button",{attrs:{size:"small",type:"primary",icon:"el-icon-search"},on:{click:function(e){return t.search()}}},[t._v("搜索")])],1)]),t._v(" "),a("footer",[a("table",{staticClass:"PI_table"},[a("tr",{staticClass:"title",staticStyle:{"text-indent":"-25vw"}},[a("el-button",{staticClass:"Btn",attrs:{type:"primary",size:"small"},on:{click:function(e){return t.openAdd()}}},[t._v("新增产品")]),t._v(" "),a("el-button",{staticClass:"Btn",attrs:{type:"primary",size:"small"},on:{click:function(e){return t.openEdit()}}},[t._v("编辑产品")]),t._v(" "),a("el-button",{staticClass:"Btn",attrs:{type:"danger",size:"small"},on:{click:function(e){return t.deletProduct()}}},[t._v("删除商品")]),t._v("\n        类别：钢木/状态：在售\n      ")],1),t._v(" "),t._m(0),t._v(" "),a("tbody",t._l(t.tableList,function(e,i){return a("tr",{key:i},[a("td",[a("div",[a("span"),t._v(" "),a("input",{staticClass:"allcheck",attrs:{type:"checkbox"},domProps:{value:e.id},on:{change:t.changeSelect}})])]),t._v(" "),a("td",[t._v("\n            "+t._s(i+1+50*(t.page-1))+"\n          ")]),t._v(" "),a("td",[t._v("\n            "+t._s(e.product_code)+"\n          ")]),t._v(" "),a("td",{attrs:{title:"点击品名进入详情"},on:{click:function(a){return t.goProductInformationDetails(a,e.product_code)}}},[t._v("\n            "+t._s(e.product_name)+"\n          ")]),t._v(" "),a("td",[t._v("\n            "+t._s(e.product_type)+"\n          ")]),t._v(" "),a("td",[t._v("\n            "+t._s(e.product_state)+"\n          ")]),t._v(" "),a("td",[t._v("\n            "+t._s(e.product_size)+"\n          ")]),t._v(" "),a("td",[t._v("\n            "+t._s(e.product_package_size)+"\n          ")]),t._v(" "),a("td",[t._v("\n            "+t._s(e.product_weight)+"\n          ")]),t._v(" "),a("td",[t._v("\n            "+t._s(e.volume)+"\n          ")])])}),0)]),t._v(" "),t.pageShow?a("el-pagination",{staticClass:"pagetotle",staticStyle:{margin:"0 auto",width:"600px","text-align":"center",background:"#fff"},attrs:{background:"","current-page":t.page,layout:"total,prev, pager, next, jumper",total:t.total,"page-size":50},on:{"current-change":t.handleCurrentChange,"update:currentPage":function(e){t.page=e},"update:current-page":function(e){t.page=e}}}):t._e()],1),t._v(" "),a("el-dialog",{attrs:{title:"编辑产品",visible:t.centerDialogVisible,"close-on-click-modal":!1,width:"400px",center:""},on:{"update:visible":function(e){t.centerDialogVisible=e}}},[a("el-form",{attrs:{inline:!0}},[a("el-form-item",{attrs:{label:"产品编码"}},[a("el-input",{attrs:{readonly:""},model:{value:t.editProductId,callback:function(e){t.editProductId=e},expression:"editProductId"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"品名"}},[a("el-input",{attrs:{type:"textarea",rows:3,readonly:""},model:{value:t.editProductName,callback:function(e){t.editProductName=e},expression:"editProductName"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"类型"}},[a("el-input",{attrs:{readonly:""},model:{value:t.editProductType,callback:function(e){t.editProductType=e},expression:"editProductType"}})],1),t._v(" "),a("el-form-item",{staticClass:"sizeList",attrs:{label:"产品尺寸"}},[a("el-input",{model:{value:t.editProductSize1,callback:function(e){t.editProductSize1=e},expression:"editProductSize1"}}),t._v(" "),a("span",[t._v("*")]),t._v(" "),a("el-input",{model:{value:t.editProductSize2,callback:function(e){t.editProductSize2=e},expression:"editProductSize2"}}),t._v(" "),a("span",[t._v("*")]),t._v(" "),a("el-input",{model:{value:t.editProductSize3,callback:function(e){t.editProductSize3=e},expression:"editProductSize3"}})],1),t._v(" "),a("el-form-item",{staticClass:"sizeList",attrs:{label:"包装尺寸"}},[a("el-input",{model:{value:t.editProductPackSize1,callback:function(e){t.editProductPackSize1=e},expression:"editProductPackSize1"}}),t._v(" "),a("span",[t._v("*")]),t._v(" "),a("el-input",{model:{value:t.editProductPackSize2,callback:function(e){t.editProductPackSize2=e},expression:"editProductPackSize2"}}),t._v(" "),a("span",[t._v("*")]),t._v(" "),a("el-input",{model:{value:t.editProductPackSize3,callback:function(e){t.editProductPackSize3=e},expression:"editProductPackSize3"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"重量(kg)"}},[a("el-input",{model:{value:t.editproductWeight,callback:function(e){t.editproductWeight=e},expression:"editproductWeight"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"状态"}},[a("el-select",{model:{value:t.editState,callback:function(e){t.editState=e},expression:"editState"}},t._l(t.productStateList,function(t,e){return a("el-option",{key:e,attrs:{value:t.value,label:t.label}})}),1)],1),t._v(" "),a("el-form-item",{staticClass:"lastBtnGroup"},[a("el-button",{attrs:{type:"primary"},on:{click:function(e){return t.editSubmit()}}},[t._v("提 交")]),t._v(" "),a("el-button",{attrs:{type:"warning"},on:{click:function(e){return t.editReset()}}},[t._v("重 置")])],1)],1)],1),t._v(" "),a("el-dialog",{attrs:{title:"新增产品",visible:t.centerDialogVisible2,width:"400px","close-on-click-modal":!1,center:""},on:{"update:visible":function(e){t.centerDialogVisible2=e}}},[a("el-form",{attrs:{inline:!0}},[a("el-form-item",{attrs:{label:"产品编码"}},[a("el-input",{model:{value:t.addProductId,callback:function(e){t.addProductId=e},expression:"addProductId"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"品名"}},[a("el-input",{attrs:{rows:3,type:"textarea"},model:{value:t.addProductName,callback:function(e){t.addProductName=e},expression:"addProductName"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"类型"}},[a("el-select",{model:{value:t.addProductType,callback:function(e){t.addProductType=e},expression:"addProductType"}},t._l(t.productTypeList,function(t,e){return a("el-option",{key:e,attrs:{value:t.value,label:t.label}})}),1)],1),t._v(" "),a("el-form-item",{staticClass:"sizeList",attrs:{label:"产品尺寸"}},[a("el-input",{model:{value:t.addProductSize1,callback:function(e){t.addProductSize1=e},expression:"addProductSize1"}}),t._v(" "),a("span",[t._v("*")]),t._v(" "),a("el-input",{model:{value:t.addProductSize2,callback:function(e){t.addProductSize2=e},expression:"addProductSize2"}}),t._v(" "),a("span",[t._v("*")]),t._v(" "),a("el-input",{model:{value:t.addProductSize3,callback:function(e){t.addProductSize3=e},expression:"addProductSize3"}})],1),t._v(" "),a("el-form-item",{staticClass:"sizeList",attrs:{label:"包装尺寸"}},[a("el-input",{model:{value:t.addProductPackSize1,callback:function(e){t.addProductPackSize1=e},expression:"addProductPackSize1"}}),t._v(" "),a("span",[t._v("*")]),t._v(" "),a("el-input",{model:{value:t.addProductPackSize2,callback:function(e){t.addProductPackSize2=e},expression:"addProductPackSize2"}}),t._v(" "),a("span",[t._v("*")]),t._v(" "),a("el-input",{model:{value:t.addProductPackSize3,callback:function(e){t.addProductPackSize3=e},expression:"addProductPackSize3"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"重量(kg)"}},[a("el-input",{model:{value:t.productWeight,callback:function(e){t.productWeight=e},expression:"productWeight"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"状态"}},[a("el-select",{model:{value:t.addState,callback:function(e){t.addState=e},expression:"addState"}},t._l(t.productStateList,function(t,e){return a("el-option",{key:e,attrs:{value:t.value,label:t.label}})}),1)],1),t._v(" "),a("el-form-item",{staticClass:"lastBtnGroup"},[a("el-button",{attrs:{type:"primary"},on:{click:function(e){return t.addSubmit()}}},[t._v("提 交")]),t._v(" "),a("el-button",{attrs:{type:"warning"},on:{click:function(e){return t.addReset()}}},[t._v("重 置")])],1)],1)],1)],1)},staticRenderFns:[function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("thead",[a("tr",[a("th"),t._v(" "),a("th",[t._v("序号")]),t._v(" "),a("th",[t._v("产品编码")]),t._v(" "),a("th",[t._v("品名")]),t._v(" "),a("th",[t._v("类别")]),t._v(" "),a("th",[t._v("状态")]),t._v(" "),a("th",[t._v("产品尺寸(cm)")]),t._v(" "),a("th",[t._v("包装尺寸(cm)")]),t._v(" "),a("th",[t._v("重量(kg)")]),t._v(" "),a("th",[t._v("体积")])])])}]};var r=a("VU/8")(o,c,!1,function(t){a("+LnQ"),a("oYKd")},"data-v-5aede4e2",null);e.default=r.exports},oYKd:function(t,e){}});
//# sourceMappingURL=36.5ac2068fcf1158b2556a.js.map