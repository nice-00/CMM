
function skip(){
    window.location.href="pages/user.html"
}

(function(){
    change();
    function change(){
        //html的 font-size 的大小尺寸
        //这里的html字体大小利用了一个简单的数学公式，当我们默认设置以屏幕320px位基准此时的字体大小为20px(320    20px),那么浏览器窗口大小改变的时候新的html的fontSize（clientWidth  新的值）就是clientWidth*20/320
        document.documentElement.style.fontSize = document.documentElement.clientWidth*2.8/320 +'px';
    }
    /* 监听窗口大小发生改变时*/
    window.addEventListener('resize',change,false);
})();


function q_a(){
    var content = document.getElementById('content'),
    ms = document.getElementById('message'),
    r_img = document.getElementById('right-img'),
    l_img = document.getElementById('left-img');
    var select = 0;
    if (content.value !== '')
        select = 1
    switch (select)
    {
        case 0:
            return false;
        case 1:
            window.sessionStorage.setItem('state','1');
            ms.innerHTML+="<li class='right'><div class='right-img'>"+r_img.innerHTML+"</div><div class='right-inf'>"+content.value+"</div><br></li>";
            break;
        // case 2:
        //     ms.innerHTML+="<li class='left'><div class='left-img'>"+l_img.innerHTML+"</div><div class='left-inf'>"+content.value+"</div><br></li>";
        //     break;
    }
}
function clear(){
    var content = document.getElementById('content');
}