$(document).ready(function () {
  $("html").removeClass("load");
});
$(function () {
  $(".dropdown-form").click(function (e) {
    e.stopPropagation();
  });
  $(".social-links a").on("click", function () {
    var href = $(this).attr("href");
    var width = 820;
    var height = 420;
    var left = (screen.width - width) / 2;
    var top = (screen.height - height) / 2 - 100;

    auth_window = window.open(
      href,
      "auth_window",
      "width=" +
        width +
        ",height=" +
        height +
        ",top=" +
        top +
        ",left=" +
        left +
        "menubar=no,resizable=no,scrollbars=no,status=no,toolbar=no"
    );
    return false;
  });

  $(".q-search-call").on("click", function () {
    $(".q-search").toggleClass("open");
    setTimeout(function () {
      $(".header").toggleClass("qs");
    }, 50);
    return false;
  });

  $(".scrollup").click(function () {
    $("html, body").animate({ scrollTop: 0 }, "fast");
    return false;
  });

  var $root = $("html, body");
  $("a.anchor").click(function () {
    var href = $.attr(this, "href");
    $root.animate(
      {
        scrollTop: $(href).offset().top,
      },
      500
    );
    return false;
  });

  $(".menu-toggle").on("click", function () {
    $("#mobilemenu").toggleClass("open");
    setTimeout(function () {
      $("html").toggleClass("mm");
    }, 50);
    return false;
  });
});
$(document).ready(function () {
  /* close ads fixed */
  $(".ads-fixed .close").click(function () {
    var temp_parent = $(this).parent();
    temp_parent.remove();
    temp_parent = null;
  });
  $("#login-ajax").click(function (e) {
    e.preventDefault();
    $(this).html('<span class="loader"></span>');
    $(".login_form .message").remove();
    $.ajax({
      url: "/login/",
      method: "POST",
      data: JSON.stringify([
        $(".login_form input[name=login_username]").val(),
        $(".login_form input[name=login_password]").val(),
      ]),
      headers: {
        "Content-type": "application/json; charset=UTF-8",
        "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0]
          .value,
      },
      success: function (result) {
        console.log(result)
        if(result.authenticated == 'success'){
          $("#login-ajax").html("ورود");
          $(".login_form").prepend(
            '<label class="form-group message"><div class="alert" style="background: #40be64;padding: 10px;border-radius: 6px;color: #ffffff;">' +
              "با موفقیت وارد حساب کابری خود شدید." +
              "</div></label>"
          );
          setTimeout(()=> {
            location.replace('/profile');
          }, 500)
        }else if(result.authenticated == 'not_active'){
          $("#login-ajax").html("ورود");
          $(".login_form").prepend(
            '<label class="form-group message"><div class="alert" style="background: #e7cd57;padding: 10px;border-radius: 6px;color: #ffffff;">' +
              "حساب کاربری شما هوز فعالسازی نشده است." +
              "</div></label>"
          );
        }else{
          $("#login-ajax").html("ورود");
          $(".login_form").prepend(
            '<label class="form-group message"><div class="alert" style="background: #ff4336;padding: 10px;border-radius: 6px;color: #ffffff;">' +
              "نام کاربری یا رمز عبور نادرست است." +
              "</div></label>"
          );
        }
      },
      error: function (error) {
        $("#login-ajax").html("ثبت نام");
      },
    });
  });

  $(".screenshots > a").simpleLightbox();
  $(".b-tabs > a").click(function (e) {
    e.preventDefault();
    $(".b-tabs > a").removeClass("active");
    $(".b-cont > .tab-pane").hide();
    $(this).addClass("active");
    $($(this).attr("href")).fadeIn();
  });

  $(".spoiler .title_spoiler").click(function (e) {
    e.preventDefault();
    $(this).next().slideToggle();
  });

  $(".add-fav").click(function (e) {
    e.preventDefault();
    $("body").append('<div id="loading-layer" style="display:none;"></div>');
    $("#loading-layer").fadeIn();
    $.ajax({
      url: fiveplay.ajaxurl,
      method: "POST",
      data: {
        action: "favAjax",
        post_id: $(this).attr("data-id"),
      },
      success: function (result) {
        if (result.status == "addlist") {
          $(".add-fav > svg > use").attr("xlink:href", "#i__favfull");
        } else if (result.status == "removelist") {
          $(".add-fav > svg > use").attr("xlink:href", "#i__fav");
        } else {
          alert("Ų®Ų·Ų§");
        }
        $("#loading-layer").fadeOut("slow", function () {
          $(this).remove();
        });
      },
      error: function (error) {
        alert("Ł…Ų´Ś©Ł„Ū ŁŲ¬ŁŲÆ ŲÆŲ§Ų±ŲÆ.");
        $("#loading-layer").fadeOut("slow", function () {
          $(this).remove();
        });
      },
    });
  });

  $("#news-likes > a").click(function (e) {
    e.preventDefault();
    $("body").append('<div id="loading-layer" style="display:none;"></div>');
    $("#loading-layer").fadeIn();
    $.ajax({
      url: '/news/ajax/reactions/',
      contentType : 'application/json',
      method: "POST",
      dataType: 'json',
      data:JSON.stringify(
        {post_id: document.querySelector('.view-news').id, type: $(this).attr("data-action")}
    
      ),
      headers: {
        "Content-type": "application/json; charset=UTF-8",
        "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0]
          .value,
      },
      success: function (result) {
        $(".like-plus span").html(result.like);
        $(".like-minus span").html(result.dislike);
        $("#vote-num-id-" + $(".likes").attr("data-id")).html(
          result.like + result.dislike
        );
        
        $("#loading-layer").fadeOut("slow", function () {
          $(this).remove();
        });
      },
      error: function (error) {
        alert("error.");
        $("#loading-layer").fadeOut("slow", function () {
          $(this).remove();
        });
      },
    });
  });

  $("#app-likes > a").click(function (e) {
    e.preventDefault();
    $("body").append('<div id="loading-layer" style="display:none;"></div>');
    $("#loading-layer").fadeIn();
    $.ajax({
      url: '/apps/reactions/',
      contentType : 'application/json',
      method: "POST",
      dataType: 'json',
      data:JSON.stringify(
        {app_id: document.querySelector('.view-app').id, type: $(this).attr("data-action")}
    
      ),
      headers: {
        "Content-type": "application/json; charset=UTF-8",
        "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0]
          .value,
      },
      success: function (result) {
        $(".like-plus span").html(result.like);
        $(".like-minus span").html(result.dislike);
        $("#vote-num-id-" + $(".likes").attr("data-id")).html(
          result.like + result.dislike
        );
        const plus = Number(document.querySelector('.like-plus').querySelector('span').textContent);
        const minus = Number(document.querySelector('.like-minus').querySelector('span').textContent);
        document.querySelector('.rating_progress_bar').querySelector('b').textContent = `محبوبیت ${Math.round((plus / (plus + minus)) * 100 )}%`;
        document.querySelector('.rating_progress_bar').querySelector('span').style.width = `${Math.round( (plus / (plus + minus)) * 100 )}%`;
        
        $("#loading-layer").fadeOut("slow", function () {
          $(this).remove();
        });
      },
      error: function (error) {
        alert("error.");
        $("#loading-layer").fadeOut("slow", function () {
          $(this).remove();
        });
      },
    });
  });
});
function setCookie(name, value, days) {
  var expires = "";
  if (days) {
    var date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
  var nameEQ = name + "=";
  var ca = document.cookie.split(";");
  // the following code allows multiple cookie values and splits them apart
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == " ") c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
}
function eraseCookie(name) {
  document.cookie = name + "=; Max-Age=-99999999;";
}
const g = (i) => document.getElementById(i),
  classes = g("h").classList,
  cl = "darktheme";

if(!localStorage.getItem('dark')){
  localStorage.setItem('dark', 'off')
}else{
  if(localStorage.getItem('dark') == 'off'){
    classes.remove(cl);
  }else if(localStorage.getItem('dark') == 'on'){
    classes.add(cl);
  }
}


g("toggle-darkmod").addEventListener("click", function (e) {
  e.preventDefault();

  if(localStorage.getItem('dark') == 'off'){
    localStorage.setItem('dark' , 'on')
    classes.add(cl);
  }else if(localStorage.getItem('dark') == 'on'){
    localStorage.setItem('dark' , 'off')
    classes.remove(cl);
  }

});
