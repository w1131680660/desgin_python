webpackJsonp([73],{KXcg:function(t,e){},UQfu:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i={mounted:function(){this.getEchartData()},methods:{getEchartData:function(){var t=this.$refs.chart;if(t){var e=this.$echarts.init(t);e.setOption({title:{text:"折线图堆叠"},tooltip:{trigger:"axis"},legend:{data:["邮件营销","联盟广告","视频广告","直接访问","搜索引擎"]},grid:{left:"3%",right:"4%",bottom:"3%",containLabel:!0},toolbox:{feature:{saveAsImage:{}}},xAxis:{type:"category",boundaryGap:!1,data:["周一","周二","周三","周四","周五","周六","周日"]},yAxis:{type:"value"},series:[{name:"邮件营销",type:"line",stack:"总量",data:[120,132,101,134,90,230,210]},{name:"联盟广告",type:"line",stack:"总量",data:[220,182,191,234,290,330,310]},{name:"视频广告",type:"line",stack:"总量",data:[150,232,201,154,190,330,410]},{name:"直接访问",type:"line",stack:"总量",data:[320,332,301,334,390,330,320]},{name:"搜索引擎",type:"line",stack:"总量",data:[820,932,901,934,1290,1330,1320]}]}),window.addEventListener("resize",function(){e.resize()})}this.$on("hook:destoryed",function(){window.removeEventListener("resize",function(){myChart.resize()})})}}},n={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",{staticClass:"con"},[e("h1",[this._v("这里是echarts测试")]),this._v(" "),e("div",{ref:"chart",staticStyle:{width:"100%",height:"376px"}})])},staticRenderFns:[]};var s=a("VU/8")(i,n,!1,function(t){a("KXcg")},null,null);e.default=s.exports}});
//# sourceMappingURL=73.1c7ed9099a60d9f955b2.js.map