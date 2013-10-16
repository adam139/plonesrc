/*jshint sub:true*/
function closeEventMore() {
    $("#cata_more_div").hide();
    $("#address_more_div").hide();
}

function innerMoreArea() {        
     var action = $("#ajaxmorearea").attr('data-ajax-target');
     var senddata = {"demo":2}	;
     $.post(action, 
           senddata,
           function(data) {
           try {
                $("#addressSearchMore1").html("");
                var str = data['provincelist'];
                $(str).appendTo("#province_list_div");
                $("#li_province_more").hide();              

            } catch (e) {
                alert(e)
            }
            },
            'json');
}

function closeSearchEventsDiv(flag) {
    if (flag == 1) {
        $("#dateSearch").val("0");
        $("#dateRangeSearchUl > .over").removeClass("over");
        $("#dateRangeSearchUl").find("li[name='0']").addClass("over");
        searchEvent();
    } else if (flag == 2) {
        $("#addressSearch").val("0");
        $("#addressSelectSearch li> .over").removeClass("over");
        $("#addressSelectSearch").find("li span[name='0']").addClass("over");
        searchEvent();
    } else if (flag == 3) {
        $("#categorySearch").val("0");
        $("#categorySelectSearch li> .over").removeClass("over");
        $("#categorySelectSearch").find("li span[name='0']").addClass("over");
        searchEvent();
    }
}

// base lib
function searchEventParent() {
    searchEvent()
}
// read query string
$.extend({
  getUrlVars: function(){
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
      hash = hashes[i].split('=');
      vars.push(hash[0]);
      vars[hash[0]] = hash[1];
    }
    return vars;
  },
  getUrlVar: function(name){
    return $.getUrlVars()[name];
  }
});

var searchEvent = function(jumpPage, rows, initKeyword) {
    var keyword;
    if (initKeyword !== undefined && initKeyword !== "") {
        keyword = initKeyword
    } else {
        keyword = $("#searchKeyword").val()
    }
    var dateSearchType = $("#dateSearch").val();
    var address = $("#addressSearch").val();
    var categoryId = $("#categorySearch").val();   
    var sortColumn = $("#solrSortColumn").val();    
    var sortDirection = $("#solrSortDirection").val();
        
    var data = {'datetype':dateSearchType,'province':address,'type':categoryId};
    data['sortcolumn'] = sortColumn;
    data['sortdirection'] = sortDirection;    
    
    if (keyword === undefined || keyword === null || keyword === "") {
           data['searchabletext'] = "";
    } else {
           data['searchabletext'] = keyword;
    }
    if (jumpPage !== undefined && jumpPage !== "") 
    {   var start = jumpPage > 0 ? (jumpPage - 1) * rows : 0;
        data['start'] = start;
        data['size'] = rows;
    } else {
        data['start'] = 0;
        data['size'] =10;
    }        
       var action = $("#ajaxsearch").attr('data-ajax-target');
       $.post(action, 
           data,
           function(resp) {
                       try {
                showSearchEventResult(resp, true, keyword)
                showResultRemind(keyword, dateSearchType, address, categoryId)
            }
                       catch(e){alert(e)}
                       },
            'json'); 
//    var searchCount = 0;
//    showResultRemind(keyword, dateSearchType, address, categoryId)
};
var totalCountSearchEvent = 0;
var showSearchEventResult = function(D, u, C) {
//function showSearchEventResult(D, u, C) {
//D json response
// u true
// c keyword
//size batch size
//start batch start
//total return result total

    var a = "";
    var h = "";
    var o = parseInt(D['size'],10);
    var l = parseInt(D['start'],10);
    var p = parseInt(D['total'],10);
    totalCountSearchEvent = p;
    var e = (l + o) > p ? (p - l) : o;

    if (e > 0) {
        generatePageLink(l, o, p); 
       a +=  D['searchresult']; 
    } else {
     document.getElementById("bottomPageId").innerHTML = "";

        a += '<tr class="div_tip">';
        a += '<td class="alert alert-block span12" colspan="7">警告！：没有搜索到您要找的信息。</td></tr>'
    }

$("#searchResultDiv").html(a);
};

function showResultRemind(d, a, c, e) {
// d search by keyword
// a search by Date
// c search by Address
// e search by type
    var b = "";
    if (d === "" && (a != "0" || c != "0" || e != "0")) {
        b = createStringSearch(d, a, c, e)
    } else {
        if (d !== "" && (a != "0" || c != "0" || e != "0")) {
            b = createStringSearch(d, a, c, e)
        }
    }
    if (d === "" && a == "0" && c == "0" && e == "0") {
        b = "<li class='a'>已选择：</li><li id='show_site_result'></li><li class='info' id='searchresultinfor'>“<span id='keyworkshow'>所有</span>”的活动信息有“<span id='searchresult_count'>" + totalCountSearchEvent + "</span>”条！</li>"
    }
    if (d !== "" && a == "0" && c == "0" && e == "0") {
        b = "<li class='a'>已选择：</li><li id='show_site_result'></li><li class='info' id='searchresultinfor'>有关“<span id='keyworkshow'>" + d + "</span>”的活动信息有“<span id='searchresult_count'>" + totalCountSearchEvent + "</span>”条！</li>"
    }
//    document.getElementById("all_result_recordinfo").innerHTML = b
    $("#all_result_recordinfo").html(b)
}

var generatePageLink = function(c, n, a) {
    var f = $("#bottomPageId");
    var k = Math.floor(a / n) + (a % n === 0 ? 0 : 1);
    if (k === 0) {
        k = 1
    }
    var l = Math.floor(c / n) + 1;
    var j = $("#fastPageList");
    j.html("");
    var d = "";
    var e = "";
    var m = $("#searchtext").val();
    if (m === undefined || m == null || m === "") {
        m = ""
    }
    if (l <= 1) {
        e += "<a href='javascript:void(0)'><img src='++resource++collective.conference/event_list_bg10.png'/></a>";
        d += "<a href='javascript:void(0)' class='page'>首页</a>";
        d += "<a href='javascript:void(0)' class='page'>上一页</a>"
    } else {
        e += "<a href='javascript:searchEvent(" + (l - 1) + ",10)'><img src='++resource++collective.conference/event_list_bg10.png'/></a>";
        d += "<a href=javascript:searchEvent(1,10) class='page'>首页</a><a href=javascript:searchEvent(" + (l - 1) + ",10) class='page'>上一页</a>"
    }
    e += "<span>" + l + "/" + k + "</span>";
    var b = 1;
    var h = 3;
    if (l == 1) {
        b = 1;
        h = l + 2;
        if (h >= k) {
            h = k
        }
    } else {
        if (l == k) {
            b = k - 2;
            if (b <= 0) {
                b = 1
            }
            h = k
        } else {
            b = l - 1;
            h = l + 1
        }
    }
    for (var g = b; g <= h; g++) {
        if (l == g) {
            d += "<a href='#' class='page_over num active'>" + g + "</a>"
        } else {
            d += "<a href=javascript:searchEvent(" + g + ",10) class='page num'>" + g + "</a>"
        }
    }
    if (l == k || k < 2) {
        e += "<a href='javascript:void(0)'><img src='++resource++collective.conference/event_list_bg11.png'/></a>";
        d += "<a href='javascript:void(0)' class='page'>下一页</a>";
        d += "<a href='javascript:void(0)' class='page'>末页</a>"
    } else {
        e += "<a href='javascript:searchEvent(" + (l + 1) + ",10)'><img src='++resource++collective.conference/event_list_bg11.png'/></a>";
        d += "<a href=javascript:searchEvent(" + (l + 1) + ",10) class='page'>下一页</a><a href=javascript:searchEvent(" + (k) + ",10) class='page'>末页</a>"
    }
   f.html(d);
   j.html(e);
};


function createStringSearch(d, a, c, g) {
    var b = "<li class='a'>已选择：</li><li id='show_site_result'>";
    var h = "";
    switch (a) {
    case "1":
        h = "1天内";
        b += "<div class='select'  onclick=\"closeSearchEventsDiv(1)\" >时间：<span id='search_site_desc' style='cursor: pointer;vertical-align: middle;'>" + h + " </span></div>";
        break;
    case "2":
        h = "2天内";
        b += "<div class='select'  onclick=\"closeSearchEventsDiv(1)\" >时间：<span  style='cursor: pointer;vertical-align: middle;'>" + h + " </span></div>";
        break;
    case "3":
        h = "7天内";
        b += "<div class='select' onclick=\"closeSearchEventsDiv(1)\">时间：<span  style='cursor: pointer;vertical-align: middle;'>" + h + " </span></div>";
        break;
    case "4":
        h = "30天内";
        b += "<div class='select' onclick=\"closeSearchEventsDiv(1)\">时间：<span style='cursor: pointer;vertical-align: middle;'>" + h + " </span></div>";
        break;
    case "5":
        h = "30天后";
        b += "<div class='select' onclick=\"closeSearchEventsDiv(1)\">时间：<span style='cursor: pointer;vertical-align: middle;'>" + h + " </span></div>";
        break
    }
    var f = "";
    if (c == "0") {
        f = "所有"
    } else {
        f = $(document.getElementById("addressSelectSearch")).find("span[name='" + c + "'] a").html();
        b += "<div class='select' onclick=\"closeSearchEventsDiv(2)\">地点：<span style='cursor: pointer;vertical-align: middle;' >" + f + " </span></div>"
    }
    var e = "";
    if (g == "0") {
        e = "所有"
    } else {
        e = $(document.getElementById("categorySelectSearch")).find("span[name='" + g + "'] a").html();
        b += "<div class='select' onclick=\"closeSearchEventsDiv(3)\">分类：<span style='cursor: pointer;vertical-align: middle;' >" + e + " </span></div>"
    }
    if (d === "") {
        b += "</li><li class='info' id='searchresultinfor'>的信息有“<span id='searchresult_count'>" + totalCountSearchEvent + "</span>”条！</li>"
    } else {
        b += "</li><li class='info' id='searchresultinfor'>中有关“<span>" + d + "</span>”的信息有“<span id='searchresult_count'>" + totalCountSearchEvent + "</span>”条！</li>"
    }
    return b
}	


$(document).ready(function(){
// read query string
// Getting URL var by its nam
    var byName = $.getUrlVar('orgname');
    if (byName === undefined || byName == null || byName === "") {
               searchEvent();
    } else {
               var byName2 = decodeURIComponent(byName);
               $("#searchKeyword").val(byName2);    
               searchEvent();
    }

    $("#dateRangeSearchUl li").live("click",function() {        
                 if ($(this).attr("class") == "title") {} else {
                    $("#dateRangeSearchUl > .over").removeClass("over");
                    $(this).addClass("over");
                    $("#dateSearch").attr("value", $(this).attr("name"));
                    searchEvent();}       
       return false;
    });

   $("#addressSelectSearch li span").live("click",function() {
                if ($(this).attr("class") == "title" || $(this).attr("class") == "more") {} else 
                {
                    $("#addressSelectSearch li> .over").removeClass("over");
                    $(this).addClass("over");
                    $("#addressSearch").attr("value", $(this).attr("name"));
                    searchEvent();
                    document.getElementById("address_more_div").style.display = "none"
                }
       return false; 
    }); 
   $("#categorySelectSearch li span").live("click",function() {    
                    if ($(this).attr("class") == "title" || $(this).attr("class") == "more") {} else 
                    {
                    $("#categorySelectSearch li> .over").removeClass("over");
                    $(this).addClass("over");
                    $("#categorySearch").attr("value", $(this).attr("name"));
                    searchEvent();
                    document.getElementById("cata_more_div").style.display = "none"
                }
       return false; 
    });                 

   $("#eventListSort a").live("click",function() {             
                $("#solrSortColumn").attr("value", $(this).attr("name"));
                if ($(this).attr("class") == "a") {
                    $(this).attr("class", "b");
                    $("#solrSortDirection").attr("value", "ascending")
                } else {
                    $(this).attr("class", "a");
                    $("#solrSortDirection").attr("value", "reverse")
                }
                searchEvent();
       return false; 
        });
        
   $("#eventListSort a").live("click",function() { 
                $("#eventListSort > .over").removeClass("over");
                $("#eventListSort a").attr("style", "");
                $(this).attr("style", "font-weight:bold;color:#279006;");
       return false;               
        }); 
                 
});