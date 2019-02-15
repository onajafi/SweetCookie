
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



function give_ALL_THE_data_in_row(ref,row_num){
    lunch_block_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > td:nth-child(2)';
    dinner_block_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > td:nth-child(3)';
    date_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > th';
    temp_output = {};
    if(ref.exists(date_selector)){
        // ref.echo(ref.getElementInfo(date_selector).text);
        ref.echo(ref.getElementInfo(date_selector).text.match(week_regex));
        ref.echo(ref.getElementInfo(date_selector).text.match(date_regex));
        temp_output["day"] = ref.getElementInfo(date_selector).text.match(week_regex)[0];
        temp_output["date"] = ref.getElementInfo(date_selector).text.match(date_regex)[0];
    }
    else{
        temp_output["day"] = "";
        temp_output["date"] = "";
    }

    temp_output["lunch_arr"] = [];
    if(ref.exists(lunch_block_selector)) {
        ref.echo(ref.getElementInfo(lunch_block_selector).text);
        for(var i=1;;i++) {
            meal_selector = lunch_block_selector + '> div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + i + ')';
            if (ref.exists(meal_selector)) {
                var temp_meal = {};
                meal_dat = ref.getElementInfo(meal_selector);
                ref.echo("++++" + i);
                ref.echo(meal_dat.text);
                temp_meal["meal_name"] = meal_dat.text;

                //Check if it has been reserved:
                if(ref.exists(meal_selector + '> span.fa.fa-check.fa-lg.has-left-margin.has_tooltip')){
                    ref.echo('CONFIRMED!');
                    temp_meal["status"] = "OK_DONE";
                }
                else if(ref.exists(meal_selector + '> span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip')){
                    ref.echo("You can still get it...");
                    temp_meal["status"] = "AWAITING";
                }
                else if(ref.exists(meal_selector + '> span.fa.fa-times-circle.fa-lg.has-left-margin.cursor_pointer.has_tooltip')){
                    ref.echo('Confirmed - But may get canceled...');
                    temp_meal["status"] = "OK_AWAITING";
                }
                else{
                    ref.echo("Nope you lost it!!!");
                    temp_meal["status"] = "FAILED";
                }
                temp_output["lunch_arr"].push(temp_meal);
            }else {
                break;
            }
        }
    }else{
        // ref.echo("INCORRECT ROW NUMBER: " + row_num);
        ref.echo("EMPTY LUNCH ROW: " + row_num)
    }

    temp_output["dinner_arr"] = [];
    if(ref.exists(dinner_block_selector)) {
        ref.echo(ref.getElementInfo(dinner_block_selector).text);
        for(var i=1;;i++) {
            meal_selector = dinner_block_selector + '> div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + i + ')';
            if (ref.exists(meal_selector)) {
                var temp_meal = {};
                meal_dat = ref.getElementInfo(meal_selector);
                ref.echo("++++" + i);
                ref.echo(meal_dat.text);
                temp_meal["meal_name"] = meal_dat.text;

                //Check if it has been reserved:
                if(ref.exists(meal_selector + '> span.fa.fa-check.fa-lg.has-left-margin.has_tooltip')){
                    ref.echo('CONFIRMED!');
                    temp_meal["status"] = "OK_DONE";
                }
                else if(ref.exists(meal_selector + '> span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip')){
                    ref.echo("You can still get it...");
                    temp_meal["status"] = "AWAITING";
                }
                else if(ref.exists(meal_selector + '> span.fa.fa-times-circle.fa-lg.has-left-margin.cursor_pointer.has_tooltip')){
                    ref.echo('Confirmed - But may get canceled...');
                    temp_meal["status"] = "OK_AWAITING";
                }
                else{
                    ref.echo("Nope you lost it!!!");
                    temp_meal["status"] = "FAILED";
                }
                temp_output["dinner_arr"].push(temp_meal);
            }else {
                break;
            }
        }
    }else{
        // ref.echo("INCORRECT ROW NUMBER: " + row_num);
        ref.echo("EMPTY DINNER ROW: " + row_num)
    }

    return temp_output;
}



var output_for_JSON = {};

casper.start('http://dining.sharif.edu/login');



function extract_json_file(){
    var output_filename = 'output_GFC_'+parsed_input_JSON.chat_id + '.json';//GFC Get Forgotten Code
    fs.write('../tmp/'+output_filename, JSON.stringify(output_for_JSON), 'w');
}

casper.then(function() {
    var title = this.getTitle();
    this.echo('First Page: ' + title);
    if(title.search(/سامانه تغذیه/) != -1){
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
    // Logging in
    this.echo(parsed_input_JSON["pass"])
    this.echo(parsed_input_JSON["user"])
    this.echo(this.sendKeys('input#loginform-username', parsed_input_JSON["user"]));
    this.echo(this.sendKeys('input#loginform-password', parsed_input_JSON["pass"]));
    this.echo(this.getHTML('[class="btn btn-default btn-block"]'));
  }).thenClick('[class="btn btn-default btn-block"]')
  .thenOpen("http://dining.sharif.edu/admin/food/forgotten-code/forgotten-code")
  .then(function(){
    // scrape something else
    this.echo(this.getTitle());
  })
  .thenOpen("http://dining.sharif.edu/admin/food/forgotten-code/forgotten-code")
  .then(function(){
    if(this.exists('div.forgotten-code-update > div.page-title')) {
        // this.echo(this.getHTML('select#foodforgottencodesform-self_id'));
        output_for_JSON["PASSWORD_STATE"] = "CORRECT";
    }else{
        output_for_JSON["PASSWORD_STATE"] = "WRONG";
        extract_json_file();
        this.echo("wrong password or username");
    this.capture('navigation.png');
        this.exit();
    }
  })
  .then(function(){
    this.wait(3000, function(){this.echo('Waiting finished')});
  })
    .then(function(){
        this.echo("Check this out:+++++++");
        // require('utils').dump(Object.keys(this.getElementInfo('div.alert.alert-info')));

        require('utils').dump(this.getElementInfo('div.alert.alert-info')['text']);
        output_for_JSON["alert_info"] = this.getElementInfo('div.alert.alert-info')['text'];
        this.echo("_________________________");
    })
    .then(function(){//Check if the limit is not reached:
        if(this.exists('select#foodforgottencodesform-self_id')){
            output_for_JSON["LIMIT_IS_REACHED"] = "FALSE";
        }else{
            output_for_JSON["LIMIT_IS_REACHED"] = "TRUE";
            extract_json_file();
            this.exit();
        }
    })
  .then(function(){
    this.echo("------------------------------------------------");

    this.echo(this.getHTML('select#foodforgottencodesform-self_id'));
    this.evaluate(function(row_value) {
        var form = document.querySelector('select#foodforgottencodesform-self_id');
        form.selectedIndex = row_value;
        $(form).val(row_value).change();
    },parsed_input_JSON["PLCnum"]);
  })
  .then(function(){
    if(parsed_input_JSON["meal_type"] == "dinner") {
        this.echo("PPPPPPP");
        this.echo(this.getHTML('select#foodforgottencodesform-food_meal_id'));
        this.evaluate(function () {
            var form = document.querySelector('select#foodforgottencodesform-food_meal_id');
            form.selectedIndex = 2;
            $(form).val(2).change();
        });
    }
  })
  .then(function(){
      this.wait(3000, function () {this.echo('Waiting finished');});

  }).then(function(){
    this.capture('navigation.png');
      if(this.exists('#get_forgotten_code_button')){
          output_for_JSON["MEAL_IS_AVAILABLE"] = "TRUE";
      } else {
          output_for_JSON["MEAL_IS_AVAILABLE"] = "FALSE";
          extract_json_file();
          this.exit();
      }
    })
    .then(function () {
        output_for_JSON["meal_name"] = this.getElementInfo('#get_forgotten_code_button')['text']
        this.echo(output_for_JSON["meal_name"])
    })
  .thenClick('button#get_forgotten_code_button')
  .then(function(){
      for(var i=0;i<10;i++) {//wait for 10 secs in total
          this.wait(1000, function () {});
          if(this.exists('div.alert.alert-info.no-bottom-margin')){
              this.echo("found it!");
              break;
          }
      }
      this.echo('Waiting finished')
  })
  .then(function() {
      this.echo('-------------------------------------------');
      var forgotten_code = this.getElementInfo('div.alert.alert-info.no-bottom-margin > div').text;
      this.echo(forgotten_code);
      output_for_JSON["FCode"] = forgotten_code;
  })
    //Now lets get the meal name (ISSUE #1)
  // .thenOpen("http://dining.sharif.edu/admin/food/food-reserve/reserve")
  //   .then(function(){
  //   this.wait(3000, function(){this.echo('Waiting finished')});
  //   })
  //   .then(function(){
  //       this.evaluate(function(row_value) {
  //           var form = document.querySelector('select#foodreservesdefineform-self_id');
  //           form.selectedIndex = row_value;
  //           $(form).val(row_value).change();
  //
  //       },parsed_input_JSON["PLCnum"]);
  //
  //
  //   })
  //   .then(function(){
  //   this.wait(3000, function(){this.echo('Waiting finished')});
  //   })
  //   .then(function(){
  //       temp_row_data = give_ALL_THE_data_in_row(this,parsed_input_JSON["serve_day"]);
  //       if(parsed_input_JSON["meal_type"] == "lunch") {
  //           parsed_input_JSON["meal_name"] = temp_row_data["lunch_arr"]["meal_name"]
  //       } else {
  //           parsed_input_JSON["meal_name"] = temp_row_data["lunch_arr"]["meal_name"]
  //       }
  //
  //   })
  .then(function(){
    this.capture('navigation.png');

    extract_json_file();

  });

casper.run();
