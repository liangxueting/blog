/*! layer demo */

;!function(){

var gather = {
  htdy: $('html, body')
};

//一睹为快
gather.demo1 = $('#demo1');
$('.layer_tiplist1').hover( function(){
	var othis = $(this), index = othis.index('.layer_tiplist1');
  
	//默认prompt
	/*layer.prompt({title: '设置每页显示数据条数'}, function(val, index){
	  	layer.msg('每页显示 '+val+' 条数据');
        layer.close(index);
	});*/
  
	//提示	
	layer.msg('当前有人正在进行修改操作', {time: 4000, icon:0});
		
},function(){
	
});

gather.demo2 = $('#demo2');
$('.layer-demolist').on('click', function(){
  var othis = $(this), index = othis.index('.layer-demolist');
  
  //页面层-自定义
  layer.open({
	type: 1,
	title: '控制实时',
	closeBtn: 1,
	shadeClose: true,
	maxmin: true, //允许全屏最小化
	/*skin: 'yourclass',
	content: '自定义HTML内容'*/	
	skin: 'layui-layer-rim', //加上边框
	area: ['auto','auto'], //宽高
	content: $(this).next()	  
  });
  

});

  
}();