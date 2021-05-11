// TO HIDE THE SIDEBAR WHEN CLICKED ON THE OVERLAY
function clickOverlay(){
      // $(".navsidebar").hide();
      $(".navsidebar").css("width", "0")
      $(".sidebar-icon").show();
      $(".darkBackground-overlay").hide();
}

// CHECKS WHETHER THE OVERLAY EXISTS OR NOT
function overlayDoesntExist(){
      if($(".darkBackground-overlay").length == 0){
          return true;
      };
//    TO APPLY THE EVENT WHEN THE OVERLAY EXISTS INITIALLY
      $(".darkBackground-overlay").click(clickOverlay);
      return false;
}

// TO SHOW THE SIDEBAR WHEN THE SIDEBAR ICON IS CLICKED
$(".sidebar-icon").click(function(){

    $(".sidebar-icon").hide();
    // $(".navsidebar").show();
    $(".navsidebar").css("width", "200px");

//  WHEN THE DARK OVERLAY DOESN'T EXISTS, PUT THE OVERLAY ELEMENT AFTER THE
//  ELEMENT WITH THE CLASS navsidebar AND APPLIES THE EVENT
    if(overlayDoesntExist()){
        let darkOverlay = "<div class=\"darkBackground-overlay\"></div>";
        $(".navsidebar").after(darkOverlay);
        $(".darkBackground-overlay").click(clickOverlay);
    };
    $(".darkBackground-overlay").show();
});



// TO ALLOW RULE TO STAY HOVER-LIKE WHEN THE MOUSE IS HOVERING THE RULE LIST
$(".rule-lists").hover(function(){
    $(".navsidebar .lists .rule > a").removeClass("sideBarLinksColour");
    $(".navsidebar .lists .rule > a").addClass("ruleBarLink");
}, function(){
    $(".navsidebar .lists .rule > a").removeClass("ruleBarLink");
    $(".navsidebar .lists .rule > a").addClass("sideBarLinksColour")
})

// ALLOWS THE RULE LIST TO DISPLAY PROPERLY
$(".rule").hover(function(){
  $(".navsidebar").css("overflow", "visible");
}, function(){
  $(".navsidebar").css("overflow", "hidden");
})
