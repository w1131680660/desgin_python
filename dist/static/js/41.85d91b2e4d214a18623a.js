webpackJsonp([41],{ZLYr:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var l=a("BO1k"),r=a.n(l),i=a("mtWM"),n=a.n(i),o={data:function(){return{editArr:{replySite:!0,replyCountry:!0,replyPlatform:!0,replyLanguage:!0,replyGoodsNo:!0},replyGoodsNo:"",replyOrderNo:"",replySite:"",replyCountry:"",replyLanguage:"",replyBuysText:"",replyTranslateChinese:"",replyTranslateChinese2:"",replyProblemType:"",replyassociatedOperation:"",replywhiteOrBlack:"",replygoodORbad:"",replysku:"",replyPlatform:"",replyUploadPeople:"",replyProductName:"",replyProductCode:"",replyEmailTitle:"",total:0,page:1,leftNavData:[],firstNav:"",twiceNav:"",threeNav:"",tableData:[],allTextarea:[],productDo:"",partData:[],fileUrl:"",submitInEmail:"",submitOutEmail:"",submitId:"",submitWarehouseCode:"",situation:"",fileList:[],interpretBtn:!1,restaurants:[]}},methods:{createFilter:function(e){return function(t){return 0===t.value.toLowerCase().indexOf(e.toLowerCase())}},querySearch:function(e,t){var a=this.restaurants;t(e?a.filter(this.createFilter(e)):a)},getDefaultData:function(){var e=this;n()({url:this._url2+"server/customer_management/email_manage",method:"get",params:{page:1,type:"站外"}}).then(function(t){console.log(t),e.tableData=t.data.re_data,e.total=t.data.count[0].count/5;for(var a=0;a<e.tableData.length;a++)e.tableData[a].accessory_addr&&(e.tableData[a].fileLI=e.tableData[a].accessory_addr.split("@"))})},indexMethod:function(e){return e+1+50*(this.page-1)},NavClick:function(e,t,a){var l=this;this.firstNav=e,this.twiceNav=t,this.threeNav=a,n()({url:this._url2+"server/customer_management/email_manage",method:"get",params:{page:1,type:"站外",platform:this.firstNav,country:this.twiceNav,site:this.threeNav}}).then(function(e){console.log(e),l.tableData=e.data.re_data,l.$nextTick(function(){l.$refs.InboundTable.bodyWrapper.scrollTop=0}),l.total=e.data.count[0].count/5,console.log(l.tableData),l.page=1,l.situation="";for(var t=0;t<l.tableData.length;t++)l.tableData[t].accessory_addr&&(l.tableData[t].fileLI=l.tableData[t].accessory_addr.split("@"))})},fileSubmit:function(e){var t=e.target.file,a=new FormData,l=!0,i=!1,n=void 0;try{for(var o,s=r()(t);!(l=(o=s.next()).done);l=!0){var c=o.value;a.append("",c)}}catch(e){i=!0,n=e}finally{try{!l&&s.return&&s.return()}finally{if(i)throw n}}},damageCheckChange:function(){for(var e=document.querySelectorAll(".damagedCheck"),t=document.querySelectorAll(".damagedDo"),a=0;a<e.length;a++)1==e[a].checked?t[a].removeAttribute("disabled"):t[a].setAttribute("disabled","disabled")},lackCheckChange:function(){for(var e=document.querySelectorAll(".lackCheck"),t=document.querySelectorAll(".lackDo"),a=0;a<e.length;a++)1==e[a].checked?t[a].removeAttribute("disabled"):t[a].setAttribute("disabled","disabled")},noReply:function(){var e=this;this.situation="未回复",n()({url:this._url2+"server/customer_management/email_manage",method:"get",params:{page:1,type:"站外",platform:this.firstNav,country:this.twiceNav,site:this.threeNav,reply_situation:this.situation}}).then(function(t){e.tableData=t.data.re_data,e.$nextTick(function(){e.$refs.InboundTable.bodyWrapper.scrollTop=0}),e.total=t.data.count[0].count/5,console.log(e.tableData),e.page=1;for(var a=0;a<e.tableData.length;a++)e.tableData[a].accessory_addr&&(e.tableData[a].fileLI=e.tableData[a].accessory_addr.split("@"))})},replyData:function(){var e=this;this.situation="已回复",n()({url:this._url2+"server/customer_management/email_manage",method:"get",params:{page:1,type:"站外",platform:this.firstNav,country:this.twiceNav,site:this.threeNav,reply_situation:this.situation}}).then(function(t){console.log(t),e.tableData=t.data.re_data,e.$nextTick(function(){e.$refs.InboundTable.bodyWrapper.scrollTop=0}),e.total=t.data.count[0].count/5,console.log(e.tableData),e.page=1;for(var a=0;a<e.tableData.length;a++)e.tableData[a].accessory_addr&&(e.tableData[a].fileLI=e.tableData[a].accessory_addr.split("@"))})},getfilename:function(e){var t=e.lastIndexOf("/");return e.substring(t+1)},showMail:function(e,t,a,l,r,i){document.querySelector(".bottomBox").style.display="block",this.replyBuysText=e,this.fileUrl=t,this.submitInEmail=a,this.submitOutEmail=l,this.submitId=i,this.replyOrderNo="",this.replySite="",this.replyCountry="",this.replyPlatform="",this.replyLanguage="",this.replyGoodsNo="",this.replyTranslateChinese="",this.replyTranslateChinese2="",this.allTextarea=[]},getDataById:function(){var e=this;n()({url:this._url2+"server/customer_management/order_num_inquire/",method:"get",params:{order_num:this.replyOrderNo}}).then(function(t){for(var a in e.replySite="",e.replyCountry="",e.replyPlatform="",e.replyLanguage="",e.replyGoodsNo="",e.editArr)e.editArr[a]=!0;if(t.data.data.length>0)for(var l in e.replySite=t.data.data[0].site,t.data.country_dict)t.data.data[0].country_code==l&&(e.replyCountry=t.data.country_dict[l][0],e.replyLanguage=t.data.country_dict[l][1],e.replyGoodsNo=t.data.data[0].product_name+"        数量:"+t.data.data[0].quantity,e.replysku=t.data.data[0].sku,e.replyPlatform=t.data.data[0].platform,e.replyProductName=t.data.data[0].product_name,e.partData=t.data.commodity_data,e.interpret(),e.reflash());e.replySite||(e.editArr.replySite=!1),e.replyCountry||(e.editArr.replyCountry=!1),e.replyPlatform||(e.editArr.replyPlatform=!1),e.replyLanguage||(e.editArr.replyLanguage=!1),e.replyGoodsNo||(e.editArr.replyGoodsNo=!1)})},interpret:function(){var e=this;this.interpretBtn=!0,console.log(this.productDo);var t=new FormData;t.append("platform",this.replyPlatform),t.append("country",this.replyCountry),t.append("language",this.replyLanguage),t.append("content",this.replyBuysText),t.append("product_code",this.productDo),this.$axios.post(this._url2+"server/customer_management/translate_semantic_analysis/",t).then(function(t){e.replyTranslateChinese=t.data.data,console.log(t,99),e.allTextarea=t.data.tem_data,e.interpretBtn=!1;var a=t.data.re_problem_data||[];for(var l in e.restaurants=[],a){var r={},i=a[l];r.value=i.problem_type,e.restaurants.push(r)}})},elseCheckbox:function(){var e=this;if(1==document.querySelector(".elseCheckbox").checked){var t=document.querySelector(".elseTexarea").value;if(!t.trim().length)return void console.log(t.trim());console.log("发起请求？？？"),n()({url:this._url2+"server/customer_management/re_message_translate/",method:"get",params:{content:t}}).then(function(t){t.data.re_content.length>0?e.replyTranslateChinese2=t.data.re_content[0]:e.replyTranslateChinese2="",console.log(t)}),this.replyProblemType="";for(var a=document.querySelectorAll(".allDiv"),l=0;l<a.length;l++)a[l].style.backgroundColor="";console.log(t)}},submitEmail:function(){console.log("问题类型",this.replyProblemType);for(var e=0,t=document.querySelectorAll(".damagedDo"),a=document.querySelectorAll(".damagedCheck"),l=document.querySelectorAll(".damagespan"),r=document.querySelectorAll(".lackCheck"),i=document.querySelectorAll(".lackDo"),n=document.querySelectorAll(".lessspan"),o=[],s=[],c="",p=0;p<a.length;p++)if(1==a[p].checked){var u=[];u.push(l[p].innerHTML),u.push(t[p].value),o.push(u),""==t[p].value&&e++}for(var d=0;d<r.length;d++)if(1==r[d].checked){var y=[];y.push(n[d].innerHTML),y.push(i[d].value),s.push(y),""==i[d].value&&e++}if(e>=1)alert("请把勾选的缺件破损零件数量填上或者不勾选");else{for(var h=document.querySelectorAll(".allDiv"),v=0;v<h.length;v++)"skyblue"==h[v].style.backgroundColor&&(c=h[v].innerHTML);if(1==document.querySelector(".elseCheckbox").checked&&(c=document.querySelector(".elseTexarea").value),""===c)alert("请把选择回复模板或手动输入并打钩");else{var m=new FormData;m.append("product_code",this.replyProductCode),m.append("product_name",this.replyGoodsNo),m.append("Inbox_email",this.submitInEmail),m.append("outbox_email",this.submitOutEmail),m.append("order_number",this.replyOrderNo),m.append("problem_type",this.replyProblemType),m.append("related_operations",this.replyassociatedOperation),m.append("praise",this.replygoodORbad),m.append("customer_status",this.replywhiteOrBlack),m.append("lack_part",s),m.append("damaged",o),m.append("email_template",c),m.append("email_content",this.replyBuysText),m.append("customer_translation",this.replyTranslateChinese),m.append("translation_template",this.replyTranslateChinese2),m.append("email_title",this.replyEmailTitle);var _="";if(this.fileUrl){for(var f=0;f<this.fileUrl.length;f++)_+=this.fileUrl[f]+"@";_&&(_=_.substr(0,_.length-1))}m.append("attachment_address",_),m.append("sku",this.replysku),m.append("upload_people",this.replyUploadPeople),m.append("id",this.submitId);var g=this.replyPlatform.charAt(0).toUpperCase()+this.replyPlatform.slice(1);m.append("platform",g),m.append("country",this.replyCountry),m.append("site",this.replySite)}}},alldiv:function(e){if(0==document.querySelector(".elseCheckbox").checked){for(var t=document.querySelectorAll(".allDiv"),a=0;a<t.length;a++)t[a].style.backgroundColor="";t[e].style.backgroundColor="skyblue",this.replyTranslateChinese2=this.allTextarea[e].email_translation,this.replyProblemType=this.allTextarea[e].problem_type}},reflash:function(){this.replyassociatedOperation="",this.replywhiteOrBlack="",this.replygoodORbad="",this.replyGoodsNo="",this.replyTranslateChinese="",this.replyTranslateChinese2="",this.replyEmailTitle="",this.replyProblemType="",document.querySelector(".elseTexarea").value=""},replacement:function(){this.replyassociatedOperation="",this.replywhiteOrBlack="",this.replygoodORbad="",this.replyOrderNo="",this.replySite="",this.replyCountry="",this.replyPlatform="",this.replyLanguage="",this.replyUploadPeople="",this.replyTranslateChinese="",this.replyTranslateChinese2="",document.querySelector(".elseTexarea").value=""},cancel:function(){document.querySelector(".bottomBox").style.display="none"},handleCurrentChange:function(e){var t=this;""==this.situation&&(this.situation=null),this.page=e,n()({url:this._url2+"server/customer_management/email_manage",method:"get",params:{page:this.page,type:"站外",platform:this.firstNav,country:this.twiceNav,site:this.threeNav,reply_situation:this.situation}}).then(function(e){console.log(e),t.tableData=e.data.re_data,t.$nextTick(function(){t.$refs.InboundTable.bodyWrapper.scrollTop=0}),t.total=e.data.count[0].count/5;for(var a=0;a<t.tableData.length;a++)t.tableData[a].accessory_addr&&(t.tableData[a].fileLI=t.tableData[a].accessory_addr.split("@"))}),null==this.situation&&(this.situation="")}},created:function(){var e=this;this.getDefaultData(),n()({url:this._url2+"server/personnel_management/area_sign2/",method:"get"}).then(function(t){console.log(t,5),e.leftNavData=t.data.data})},mounted:function(){window.addEventListener("scroll",this.handleScroll),this.replyUploadPeople=sessionStorage.getItem("user_name")},watch:{}},s={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{attrs:{id:"InboundMail"}},[a("el-menu",{staticClass:"leftNav",attrs:{"unique-opened":""}},e._l(e.leftNavData,function(t,l){return a("el-submenu",{key:l,attrs:{index:l+""}},[a("template",{slot:"title"},[e._v(e._s(l))]),e._v(" "),e._l(t,function(t,r){return a("el-submenu",{key:r,attrs:{index:r+""}},[a("template",{slot:"title"},[e._v(e._s(r))]),e._v(" "),e._l(t,function(t,i){return a("el-menu-item",{key:i,attrs:{index:r+t},on:{click:function(a){return e.NavClick(l,r,t)}}},[e._v(e._s(t))])})],2)})],2)}),1),e._v(" "),a("div",{staticStyle:{"margin-left":"13vw","padding-top":"2vh"}},[a("h3",{staticStyle:{color:"white"}},[e._v("站外邮件回复")]),e._v(" "),a("div",{staticClass:"topOpt",staticStyle:{margin:"10px 0"}},[a("el-button",{attrs:{type:"primary"},on:{click:e.noReply}},[e._v("全部未回复")]),e._v(" "),a("el-button",{attrs:{type:"primary"},on:{click:e.replyData}},[e._v("已回复")])],1),e._v(" "),a("el-table",{ref:"InboundTable",staticStyle:{width:"99%"},attrs:{"highlight-current-row":"","max-height":"630",border:"",data:e.tableData}},[a("el-table-column",{attrs:{align:"center",type:"index",index:e.indexMethod,label:"序号",width:"60"}}),e._v(" "),a("el-table-column",{attrs:{prop:"Inbox_email",align:"center",label:"收件邮箱地址",width:"150"}}),e._v(" "),a("el-table-column",{attrs:{prop:"email_date",align:"center",label:"收件时间"}}),e._v(" "),a("el-table-column",{attrs:{prop:"outbox_email",align:"center",label:"发件人邮箱地址"}}),e._v(" "),a("el-table-column",{attrs:{prop:"platform",align:"center",label:"渠道",width:"60"}}),e._v(" "),a("el-table-column",{attrs:{prop:"site",align:"center",label:"站点",width:"60"}}),e._v(" "),a("el-table-column",{attrs:{prop:"country",align:"center",label:"国家",width:"60"}}),e._v(" "),a("el-table-column",{attrs:{prop:"order_number",align:"center",label:"订单号"}}),e._v(" "),a("el-table-column",{attrs:{prop:"email_content",align:"center",label:"邮件内容",width:"400"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-input",{attrs:{rows:4,readonly:"",type:"textarea"},model:{value:t.row.email_content,callback:function(a){e.$set(t.row,"email_content",a)},expression:"scope.row.email_content"}})]}}])}),e._v(" "),a("el-table-column",{attrs:{width:"230",align:"center",label:"附件"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("div",e._l(t.row.fileLI,function(t,l){return a("a",{key:l,attrs:{download:"",href:t,target:"_Blank"}},[e._v(e._s(e.getfilename(t))+" "),a("br")])}),0)]}}])}),e._v(" "),a("el-table-column",{attrs:{align:"center",prop:"",label:"回复情况（点击接取）"},scopedSlots:e._u([{key:"default",fn:function(t){return["未回复"==t.row.reply_situation?a("span",{staticStyle:{color:"skyblue",display:"block",width:"100%",height:"94px",cursor:"pointer","line-height":"94px"},on:{click:function(a){return e.showMail(t.row.email_content,t.row.fileLI,t.row.Inbox_email,t.row.outbox_email,t.row.platform,t.row.id)}}},[e._v("未回复")]):a("span",[e._v("已回复")])]}}])}),e._v(" "),a("el-table-column",{attrs:{align:"center",prop:"processing_time",width:"80",label:"处理时间"}}),e._v(" "),a("el-table-column",{attrs:{align:"center",prop:"dispose_person",width:"80",label:"处理人"}})],1),e._v(" "),a("el-pagination",{staticClass:"pagetotle",staticStyle:{margin:"1vh 0 0 35vw"},attrs:{background:"","current-page":e.page,layout:"prev, pager, next, jumper",total:e.total},on:{"current-change":e.handleCurrentChange}}),e._v(" "),a("div",{staticClass:"bottomBox"},[e._m(0),e._v(" "),e._m(1),e._v(" "),a("h4",{staticStyle:{margin:"2vh"}},[e._v("回复站外邮件")]),e._v(" "),a("div",{staticStyle:{margin:"2vh 0 2vh 10vh"}},[e._v("\n        订单编号："),a("el-input",{staticStyle:{width:"20vw"},attrs:{placeholder:"请输入订单编号"},model:{value:e.replyOrderNo,callback:function(t){e.replyOrderNo=t},expression:"replyOrderNo"}}),a("el-button",{staticStyle:{"margin-left":"1vw"},attrs:{type:"primary"},on:{click:function(t){return e.getDataById()}}},[e._v("查 看")])],1),e._v(" "),a("div",[a("span",{staticStyle:{margin:"10vh 10vh 5vh 10vh"}},[e._v("站点："),a("el-input",{staticStyle:{width:"10vw"},attrs:{placeholder:"请输入订单编号获取",readonly:e.editArr.replySite},model:{value:e.replySite,callback:function(t){e.replySite=t},expression:"replySite"}})],1),e._v(" "),a("span",{staticStyle:{margin:"5vh"}},[e._v("国家："),a("el-input",{staticStyle:{width:"10vw"},attrs:{placeholder:"请输入订单编号获取",readonly:e.editArr.replyCountry},model:{value:e.replyCountry,callback:function(t){e.replyCountry=t},expression:"replyCountry"}})],1),e._v(" "),a("span",{staticStyle:{margin:"5vh"}},[e._v("平台："),a("el-input",{staticStyle:{width:"10vw"},attrs:{placeholder:"请输入订单编号获取",readonly:e.editArr.replyPlatform},model:{value:e.replyPlatform,callback:function(t){e.replyPlatform=t},expression:"replyPlatform"}})],1),e._v(" "),a("span",{staticStyle:{margin:"5vh"}},[e._v("语言："),a("el-input",{staticStyle:{width:"10vw"},attrs:{placeholder:"请输入订单编号获取",readonly:e.editArr.replyLanguage},model:{value:e.replyLanguage,callback:function(t){e.replyLanguage=t},expression:"replyLanguage"}})],1),e._v(" "),a("div",{staticStyle:{margin:"5vh 0 5vh 5vw"}},[e._v("\n          上传人："),a("el-input",{staticStyle:{width:"10vw"},attrs:{placeholder:"请输入订单编号获取",readonly:""},model:{value:e.replyUploadPeople,callback:function(t){e.replyUploadPeople=t},expression:"replyUploadPeople"}})],1)]),e._v(" "),a("div",{staticStyle:{margin:"2vh 0 0 10vh"}},[e._v("\n        商品及其数量："),a("el-input",{staticStyle:{width:"30vw"},attrs:{placeholder:"请输入订单编号获取",readonly:e.editArr.replyGoodsNo},model:{value:e.replyGoodsNo,callback:function(t){e.replyGoodsNo=t},expression:"replyGoodsNo"}})],1),e._v(" "),a("div",{staticStyle:{margin:"2vh 0 0 10vh",display:"flex"}},[a("div",{staticStyle:{flex:"1"}},[e._v("\n          买家消息内容：\n          "),a("el-input",{staticStyle:{width:"20vw"},attrs:{type:"textarea",placeholder:"请输入内容",maxlength:"9999","show-word-limit":"",rows:15,readonly:""},model:{value:e.replyBuysText,callback:function(t){e.replyBuysText=t},expression:"replyBuysText"}})],1),e._v(" "),a("div",{staticStyle:{flex:"1"}},[a("el-button",{staticStyle:{margin:"17.5vh 0 0 5vw",width:"10vw"},attrs:{type:"primary",disabled:e.interpretBtn},on:{click:e.interpret}},[e._v("匹配并翻译")])],1),e._v(" "),a("div",{staticStyle:{flex:"2"}},[a("el-input",{staticStyle:{width:"35vw"},attrs:{type:"textarea",placeholder:"买家消息内容翻译",maxlength:"9999","show-word-limit":"",rows:15},model:{value:e.replyTranslateChinese,callback:function(t){e.replyTranslateChinese=t},expression:"replyTranslateChinese"}})],1)]),e._v(" "),a("div",{staticStyle:{margin:"2vh 0 0 10vh",display:"flex"}},[a("div",{staticStyle:{flex:"4",border:"1px solid #dddddd"}},[a("ul",{staticClass:"textareaall"},e._l(e.allTextarea,function(t,l){return a("li",{key:l,staticStyle:{width:"50%"}},[a("h5",{staticStyle:{padding:"0.5vh",height:"5vh"}},[e._v("\n                国家："+e._s(t.country)+"---问题类型："+e._s(t.problem_type)+"\n              ")]),e._v(" "),a("div",{staticClass:"allDiv",staticStyle:{width:"100%",height:"13vh","overflow-y":"auto"},on:{click:function(t){return e.alldiv(l)}}},[e._v("\n                "+e._s(t.email_content)+"\n              ")])])}),0),e._v(" "),a("input",{staticClass:"elseCheckbox",attrs:{type:"checkbox"},on:{click:function(t){return e.elseCheckbox()}}}),a("textarea",{staticClass:"elseTexarea",attrs:{name:"",id:"",cols:"40",rows:"8"},on:{blur:function(t){return e.elseCheckbox()}}})]),e._v(" "),a("div",{staticStyle:{flex:"5"}},[a("el-input",{staticStyle:{width:"35vw",margin:"0 0 0 4.5vw"},attrs:{type:"textarea",placeholder:"模板内容翻译",maxlength:"9999","show-word-limit":"",rows:7,readonly:""},model:{value:e.replyTranslateChinese2,callback:function(t){e.replyTranslateChinese2=t},expression:"replyTranslateChinese2"}})],1)]),e._v(" "),a("div",{staticStyle:{margin:"2vh 0 0 10vh",display:"flex"}},[a("div",{staticStyle:{flex:"4"}},[a("div",{staticStyle:{"margin-bottom":"2vh"}},[e._v("\n            邮件标题："),a("el-input",{staticStyle:{width:"20vw"},attrs:{placeholder:""},model:{value:e.replyEmailTitle,callback:function(t){e.replyEmailTitle=t},expression:"replyEmailTitle"}})],1),e._v(" "),a("div",{staticStyle:{"margin-bottom":"2vh"}},[e._v("\n            问题类型：\n            "),a("el-autocomplete",{staticClass:"inline-input",staticStyle:{width:"20vw"},attrs:{"fetch-suggestions":e.querySearch,placeholder:"请输入内容"},model:{value:e.replyProblemType,callback:function(t){e.replyProblemType=t},expression:"replyProblemType"}})],1),e._v(" "),a("div",{staticStyle:{"max-height":"15vh","overflow-y":"auto"}},[e._v("\n            缺件及其数量\n            "),a("ul",{staticClass:"lessul",staticStyle:{width:"100%"}},e._l(e.partData,function(t,l){return a("li",{key:l,staticStyle:{width:"100%"}},[a("input",{staticClass:"lackCheck",attrs:{type:"checkbox"},on:{change:e.lackCheckChange}}),a("span",{staticClass:"lessspan"},[e._v(e._s(t.part_code))]),a("input",{staticClass:"lackDo",staticStyle:{width:"40%",height:"2.5vh"},attrs:{type:"number",value:"1",disabled:""}})])}),0)]),e._v(" "),a("div",{staticStyle:{"max-height":"15vh","overflow-y":"auto","margin-top":"2vh"}},[e._v("\n            破损及其数量\n            "),a("ul",{staticClass:"badul",staticStyle:{width:"100%"}},e._l(e.partData,function(t,l){return a("li",{key:l,staticStyle:{width:"100%"}},[a("input",{staticClass:"damagedCheck",attrs:{type:"checkbox"},on:{change:e.damageCheckChange}}),a("span",{staticClass:"damagespan"},[e._v(e._s(t.part_code))]),a("input",{staticClass:"damagedDo",staticStyle:{width:"40%",height:"2.5vh"},attrs:{type:"number",value:"1",disabled:""}})])}),0)]),e._v(" "),a("div",[e._v("\n            相关操作:"),a("select",{directives:[{name:"model",rawName:"v-model",value:e.replyassociatedOperation,expression:"replyassociatedOperation"}],staticStyle:{width:"15vw",height:"3vh"},on:{change:function(t){var a=Array.prototype.filter.call(t.target.options,function(e){return e.selected}).map(function(e){return"_value"in e?e._value:e.value});e.replyassociatedOperation=t.target.multiple?a:a[0]}}},[a("option",{attrs:{value:"发新品"}},[e._v("发新品")]),e._v(" "),a("option",{attrs:{value:"退全款"}},[e._v("退全款")]),e._v(" "),a("option",{attrs:{value:"部分退款"}},[e._v("部分退款")]),e._v(" "),a("option",{attrs:{value:"退货"}},[e._v("退货")])])]),e._v(" "),a("div",[e._v("\n            客户评级:"),a("select",{directives:[{name:"model",rawName:"v-model",value:e.replywhiteOrBlack,expression:"replywhiteOrBlack"}],staticStyle:{width:"15vw",height:"3vh"},on:{change:function(t){var a=Array.prototype.filter.call(t.target.options,function(e){return e.selected}).map(function(e){return"_value"in e?e._value:e.value});e.replywhiteOrBlack=t.target.multiple?a:a[0]}}},[a("option",{attrs:{value:"白名单"}},[e._v("白名单")]),e._v(" "),a("option",{attrs:{value:"黑名单"}},[e._v("黑名单")])])]),e._v(" "),a("div",[e._v("\n            是否获得好评:"),a("select",{directives:[{name:"model",rawName:"v-model",value:e.replygoodORbad,expression:"replygoodORbad"}],staticStyle:{width:"13vw",height:"3vh"},on:{change:function(t){var a=Array.prototype.filter.call(t.target.options,function(e){return e.selected}).map(function(e){return"_value"in e?e._value:e.value});e.replygoodORbad=t.target.multiple?a:a[0]}}},[a("option",{attrs:{value:"是"}},[e._v("是")]),e._v(" "),a("option",{attrs:{value:"否"}},[e._v("否")])])])]),e._v(" "),a("div",{staticStyle:{flex:"6","margin-left":"14vw"}},[e._v("\n          附件：\n          "),e._v(" "),e._l(e.fileUrl,function(t,l){return a("a",{key:l,attrs:{href:t,download:"",target:"_Blank"}},[e._v(e._s(e.getfilename(t))+" "),a("br")])})],2)]),e._v(" "),a("div",{staticStyle:{margin:"2vh 0 0 10vh",display:"flex","margin-bottom":"5vh"}},[a("div",{staticStyle:{flex:"1"}},[a("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.submitEmail()}}},[e._v("提 交")])],1),e._v(" "),a("div",{staticStyle:{flex:"1"}},[a("el-button",{attrs:{type:"warning"},on:{click:function(t){return e.replacement()}}},[e._v("重 置")])],1),e._v(" "),a("div",{staticStyle:{flex:"1"}},[a("el-button",{attrs:{type:"danger"},on:{click:function(t){return e.cancel()}}},[e._v("取 消")])],1),e._v(" "),a("div",{staticStyle:{flex:"6"}})])])],1)],1)},staticRenderFns:[function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticStyle:{position:"absolute",top:"55vh",left:"41vw"}},[t("i",{staticClass:"el-icon-right",staticStyle:{"font-size":"2rem",color:"#66b1ff",opacity:"0.5"}})])},function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticStyle:{position:"absolute",top:"84vh",left:"41vw"}},[t("i",{staticClass:"el-icon-right",staticStyle:{"font-size":"2rem",color:"#66b1ff",opacity:"0.5"}})])}]};var c=a("VU/8")(o,s,!1,function(e){a("iZTz"),a("v3in")},"data-v-32acd172",null);t.default=c.exports},iZTz:function(e,t){},v3in:function(e,t){}});
//# sourceMappingURL=41.85d91b2e4d214a18623a.js.map