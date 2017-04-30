package com.example.samort7.androidtwinty;

import android.app.ProgressDialog;
import android.os.AsyncTask;
import android.os.Build;
import android.support.annotation.RequiresApi;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.telephony.PhoneNumberFormattingTextWatcher;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import com.amazonaws.ClientConfiguration;
import com.amazonaws.Protocol;
import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.model.ObjectMetadata;
import java.io.File;
import java.io.IOException;

import com.amazonaws.AmazonClientException;
import com.amazonaws.AmazonServiceException;
import com.amazonaws.auth.profile.ProfileCredentialsProvider;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.model.PutObjectRequest;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    ProgressDialog pd;
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
        EditText mEdit =(EditText)findViewById(R.id.editText2);
        switch (b.getId()) {
            case R.id.button:
                msgText = mEdit.getText().toString();
                break;
            case R.id.button2:
                msgText = "unfollow " + mEdit.getText().toString();
                break;
        }
        Log.d("MYAPP", msgText);
        EditText phone = (EditText) findViewById(R.id.editText);
        fromNumber = phone.getText().toString();
        fromNumber = fromNumber.replace("(","");
        fromNumber = fromNumber.replace(")","");
        fromNumber = fromNumber.replace("-","");
        fromNumber = fromNumber.replace(" ","");
        fromNumber = "+1" + fromNumber;
        Log.d("MYAPP", fromNumber);
        new JsonTask().execute("https://s3.amazonaws.com/twinty/users.json");
    }

    private class JsonTask extends AsyncTask<String, String, String> {

//        protected void onPreExecute() {
//            super.onPreExecute();
//
//            ProgressDialog pd = new ProgressDialog(MainActivity.this);
//            pd.setMessage("Please wait");
//            pd.setCancelable(false);
//            pd.show();
//        }

        @RequiresApi(api = Build.VERSION_CODES.KITKAT)
        protected String doInBackground(String... params) {

            HttpURLConnection connection = null;
            BufferedReader reader = null;

            try {
                URL url = new URL(params[0]);
                connection = (HttpURLConnection) url.openConnection();
                connection.connect();

                InputStream stream = connection.getInputStream();

                reader = new BufferedReader(new InputStreamReader(stream));

                StringBuffer buffer = new StringBuffer();
                String line = "";

                while ((line = reader.readLine()) != null) {
                    buffer.append(line+"\n");
                    Log.d("MYAPP", line);   //here you will get the whole response.

                    try {
                        Log.d("MYAPP", "Entering try for JSONObject put");
                        JSONObject obj = new JSONObject(line);

                        if (obj.has(msgText)) {

                            obj.getJSONArray(msgText).put(fromNumber);

                        }
                        else {
                            JSONArray phoneArray = new JSONArray();
                            phoneArray.put(fromNumber);
                            obj.put(msgText, phoneArray); //Adds someone to JSON list
                        }



//                        String accessKey = "AKIAJE253PUSJXRAJC2Q";
//                        String secretKey = "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";
//
//                        Log.d("MYAPP", "In Amazon area");
//                        AWSCredentials credentials = new BasicAWSCredentials(accessKey, secretKey);
//                        ClientConfiguration clientConfig = new ClientConfiguration();
//                        AmazonS3 conn = new AmazonS3Client(credentials, clientConfig);
//
//                        Log.d("MYAPP", "Before first endpoint");
//                        conn.setEndpoint("objects.dreamhost.com");
//                        clientConfig.setProtocol(Protocol.HTTP);
//
//                        conn.setEndpoint("endpoint.com");
//
//                        Log.d("MYAPP", "Writing");
//                        ByteArrayInputStream input = new ByteArrayInputStream("Hello World!".getBytes());
//                        Log.d("MYAPP", "Writing2");
//                        conn.putObject("twinty", "hello.txt", input, new ObjectMetadata());
//                        Log.d("MYAPP", "Finished writing");

//                        Log.d("MYAPP", "PreStuff");
//                        File file=new File("C:\\Users\\samor\\Desktop\\test.json");
//                        file.createNewFile();
//                        try (FileWriter fileWriterW = new FileWriter(file)) {
//                            Log.d("MYAPP", "Stuff");
//                            fileWriterW.write(obj.toString());
//                            fileWriterW.flush();
//
//                        } catch (IOException e) {
//                            e.printStackTrace();
//                        }
//
//                        Log.d("MYAPP", obj.toString());
                    } catch (JSONException e) {
                        Log.e("MYAPP", e.toString());
                    }

                }

                return buffer.toString();

            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                if (connection != null) {
                    connection.disconnect();
                }
                try {
                    if (reader != null) {
                        reader.close();
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            return null;
        }

//        @Override
//        protected void onPostExecute(String result) {
//            super.onPostExecute(result);
//            if (pd.isShowing()){
//                pd.dismiss();
//            }
////            txtJson.setText(result);
//        }
    }
}
