
var casper = require('casper').create();
var x = require('casper').selectXPath;
var fs = require('fs');

casper.echo('The inputs:');
casper.echo(casper.cli.args[0]);

//reading the input file:
var file_input = fs.read('../tmp/'+casper.cli.args[0]);
var parsed_input_JSON = JSON.parse(file_input)
// require('utils').dump(parsed_JSON.pass);
//----------------------

var output_for_JSON = {};



function extract_json_file(){
    var output_filename = 'output_RES_'+parsed_input_JSON.chat_id + '.json';
    fs.write('../tmp/'+output_filename, JSON.stringify(output_for_JSON), 'w');
}

casper.start('https://dining.sharif.ir/login');

casper.then(function() {
    var title = this.getTitle();
    this.echo('First Page: ' + title);
	this.capture('navigation.png');
    if(title.search(/میز خدمات الکترونیکی/) != -1){
        output_for_JSON["ENTRY_STATE"] = "GOOD";
    }
    else{
        this.echo("Didn't load page");
        output_for_JSON["ENTRY_STATE"] = "BAD";
        extract_json_file();
        this.exit();
    }
})
.then(function(){
    this.echo(parsed_input_JSON["pass"]);
    this.echo(parsed_input_JSON["user"]);
    this.echo(this.sendKeys('input#student_student_identifier', parsed_input_JSON["user"]));
    this.echo(this.sendKeys('input#student_password', parsed_input_JSON["pass"]));
    this.echo(this.getHTML('.btn'));
  }).thenClick('.btn')
  .thenOpen("https://dining.sharif.ir/admin/")
  .then(function(){
    // scrape something else
    this.echo(this.getTitle());
  })
  .thenOpen("https://dining.sharif.ir/admin/food/food-reserve/reserve")
  .then(function(){
    // scrape something else
    this.echo(this.getTitle());
    if(this.exists('.navigation-link:nth-child(1)')) {
        this.echo(this.getHTML('.navigation-link:nth-child(1)'));
        output_for_JSON["PASSWORD_STATE"] = "CORRECT";
    }else{
        output_for_JSON["PASSWORD_STATE"] = "WRONG";
        extract_json_file();
        this.exit();
    }
  })
  /*.thenClick('.navigation-link:nth-child(1)')*/
  .then(function(){
      for(var i=0;i<10;i++) {//wait for 10 secs in total
          this.wait(1000, function () {});
          if(this.exists('select#foodreservesdefineform-self_id')){
              break;
          }
      }
      this.echo('Waiting finished')
  })
    .then(function() {
        this.evaluate(function (row_value) {
            var form = document.querySelector('select#foodreservesdefineform-self_id');
            form.selectedIndex = row_value;
            $(form).val(row_value).change();

        }, parsed_input_JSON["PLCnum"]);
    })
    .then(function(){
        this.wait(3000, function(){this.echo('Waiting finished')});
    })
  .thenClick('.navigation-link:nth-child(1)')
  .then(function(){
    this.wait(3000, function(){this.echo('Waiting finished')});
  })
  .then(function(){
    // arrs = this.getElementsInfo('div.food-reserve-diet-div.has-mini-bottom-padding');
    // button_arr = this.getElementsInfo('span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip');
    // this.echo(arrs[2].text);
    //require('utils').dump(button_arr[0]);
    //this.echo(this.getHTML('span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip:nth-of-type('+'1'+')'));
    var order_list = parsed_input_JSON["order_list"];
    this.echo(Object.keys(order_list))

    ref = this;
    Object.keys(order_list).forEach(function(key) {
        ref.echo("IN_LOOP:")
        ref.echo(key)
        if(order_list[key] == "nevermind"){
            return;
        }
        //Find out if this is a lunch or dinner:
        var column;
        if(Number(key) < 7){
            column = '2';
            var cart_button_selector = 'tr:nth-child(' + (Number(key) + 1)
            + ') > td:nth-child('+ column +') > div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + (Number(order_list[key]) + 1)
            + ') > span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip';
        }else if(Number(key) < 14){
            column = '3';
            var cart_button_selector = 'tr:nth-child(' + (Number(key) -6)
            + ') > td:nth-child('+ column +') > div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + (Number(order_list[key]) + 1)
            + ') > span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip';
        }else if(Number(key) < 21){
            column = '4';
            var cart_button_selector = 'tr:nth-child(' + (Number(key) -13)
            + ') > td:nth-child('+ column +') > div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + (Number(order_list[key]) + 1)
            + ') > span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip';
        }else if(Number(key) < 28){
            column = '5';
            var cart_button_selector = 'tr:nth-child(' + (Number(key) -20)
            + ') > td:nth-child('+ column +') > div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + (Number(order_list[key]) + 1)
            + ') > span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip';
        }


        if(ref.exists(cart_button_selector)) {
            ref.thenClick(cart_button_selector);
            ref.echo("FOUND: " + key + " - " + order_list[key])
            button_arr = ref.getElementsInfo(cart_button_selector);
            require('utils').dump(button_arr[0]);
        }else{
            ref.echo("Didn't find the button: " + key + " - " + order_list[key])
        }
    });

    // for(var key in Object.keys(order_list)) {
    //     this.echo("IN_LOOP:")
    //     this.echo(key)
    //     if(order_list[key] == "nevermind"){
    //         continue;
    //     }
    //     var cart_button_selector = 'tr:nth-child(' + (Number(key) + 1)
    //         + ') > td.text-right > div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + (Number(order_list[key]) + 1)
    //         + ') > span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip';
    //
    //     if(this.exists(cart_button_selector)) {
    //         this.thenClick(cart_button_selector);
    //         this.echo("FOUND: " + key + " - " + order_list[key])
    //     }else{
    //         this.echo("Didn't find the button: " + key + " - " + order_list[key])
    //     }
    // }
  })
  .then(function(){
    this.wait(3000, function(){this.echo('Waiting finished')});
  })
  .then(function(){
    // arrs = this.getElementsInfo('div.food-reserve-diet-div.has-mini-bottom-padding');
    // button_arr = this.getElementsInfo('span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip');
    // this.echo(arrs[2].text);
    //require('utils').dump(button_arr[0]);
    //this.echo(this.getHTML('span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip:nth-of-type('+'1'+')'));
    var order_list = parsed_input_JSON["order_list"];
    this.echo(Object.keys(order_list))

    ref = this;
    Object.keys(order_list).forEach(function(key) {
        ref.echo("IN_LOOP:")
        ref.echo(key)
        if(order_list[key] == "nevermind"){
            return;
        }
        //Find out if this is a lunch or dinner:
        var column;
        if(Number(key) < 7){
            column = '2';
            var cart_button_selector = 'tr:nth-child(' + (Number(key) + 1)
            + ') > td:nth-child('+ column +') > div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + (Number(order_list[key]) + 1)
            + ') > span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip';
        }else if(Number(key) < 14){
            column = '3';
            var cart_button_selector = 'tr:nth-child(' + (Number(key) -6)
            + ') > td:nth-child('+ column +') > div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + (Number(order_list[key]) + 1)
            + ') > span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip';
        }else if(Number(key) < 21){
            column = '4';
            var cart_button_selector = 'tr:nth-child(' + (Number(key) -13)
            + ') > td:nth-child('+ column +') > div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + (Number(order_list[key]) + 1)
            + ') > span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip';
        }else if(Number(key) < 28){
            column = '5';
            var cart_button_selector = 'tr:nth-child(' + (Number(key) -20)
            + ') > td:nth-child('+ column +') > div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + (Number(order_list[key]) + 1)
            + ') > span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip';
        }


        if(ref.exists(cart_button_selector)) {
            ref.thenClick(cart_button_selector);
            ref.echo("FOUND: " + key + " - " + order_list[key])
            button_arr = ref.getElementsInfo(cart_button_selector);
            require('utils').dump(button_arr[0]);
        }else{
            ref.echo("Didn't find the button: " + key + " - " + order_list[key])
        }
    });

    // for(var key in Object.keys(order_list)) {
    //     this.echo("IN_LOOP:")
    //     this.echo(key)
    //     if(order_list[key] == "nevermind"){
    //         continue;
    //     }
    //     var cart_button_selector = 'tr:nth-child(' + (Number(key) + 1)
    //         + ') > td.text-right > div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + (Number(order_list[key]) + 1)
    //         + ') > span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip';
    //
    //     if(this.exists(cart_button_selector)) {
    //         this.thenClick(cart_button_selector);
    //         this.echo("FOUND: " + key + " - " + order_list[key])
    //     }else{
    //         this.echo("Didn't find the button: " + key + " - " + order_list[key])
    //     }
    // }
  })
  .then(function(){
    // scrape something else
    //this.echo(this.getTitle());
    //this.echo(this.getHTML('[class="table sharif-table table-bordered table-condensed"]'));
    this.echo("_________________________________________________");
    this.capture('navigation.png');
    extract_json_file();
    // this.echo(this.getHTML(x("//body//form")));
    //this.echo(this.getHTML(x("//body//form//div[class='reserve-table']")));
  });

casper.run();
