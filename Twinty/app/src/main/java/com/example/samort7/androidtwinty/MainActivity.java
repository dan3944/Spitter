package com.example.samort7.androidtwinty;

import android.content.Context;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.telephony.PhoneNumberFormattingTextWatcher;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.URL;
import javax.net.ssl.HttpsURLConnection;

import static com.example.samort7.androidtwinty.R.id.editText;
import static com.example.samort7.androidtwinty.R.id.editText2;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    String fromNumber;
    String msgText;
    String handle;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        Button button1 = (Button) findViewById(R.id.button);
        button1.setOnClickListener(this);
        Button button2 = (Button) findViewById(R.id.button2);
        button2.setOnClickListener(this);

        EditText phone = (EditText) findViewById(R.id.editText);
        phone.addTextChangedListener(new PhoneNumberFormattingTextWatcher());

    }

    @Override
    public void onClick(View b) {
        switch (b.getId()) {
            case R.id.button:
                msgText = "follow " + Integer.toString(editText2);
                break;
            case R.id.button2:
                msgText = "unfollow " + Integer.toString(editText2);
                break;
        }
        fromNumber = Integer.toString(editText);
        JSONObject jo = new JSONObject();
        try {
            jo.put("fromNumber", fromNumber);
            jo.put("msgText", msgText);
        } catch (JSONException e) {
            Log.e("MYAPP", "unexpected JSON exception", e);
        }
        try {
            httpPost(jo);
        } catch (java.lang.Exception e){
            Log.e("MYAPP", "unexpected JSON exception", e);
        }
    }

    private void httpPost(JSONObject params) throws Exception {
        String url = "https://candidate.hubteam.com/candidateTest/v2/results?userKey=79e24b6dd5c920f00520ebb5f474";
        URL obj = new URL(url);
        HttpsURLConnection con = (HttpsURLConnection) obj.openConnection();

        //add request header
        con.setRequestMethod("POST");
        con.setRequestProperty("Accept-Language", "en-US,en;q=0.5");

        // Send post request
        con.setDoOutput(true);
        DataOutputStream wr = new DataOutputStream(con.getOutputStream());
        wr.writeBytes(params.toString());
        wr.flush();
        wr.close();

        BufferedReader in = new BufferedReader(
                new InputStreamReader(con.getInputStream()));
        String inputLine;
        StringBuffer response = new StringBuffer();

        while ((inputLine = in.readLine()) != null) {
            response.append(inputLine);
        }
        in.close();
    }
}
