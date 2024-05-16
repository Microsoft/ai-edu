using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace TTS_Demo
{

        
    class TTSApi
    {
        //语言配置信息
        string locale = "zh-CN";
        string voiceName = "Microsoft Server Speech Text to Speech Voice (zh-CN, HuihuiRUS)";
      
        string accessToken;
        Authentication auth = new Authentication("https://******/sts/v1.0/issuetoken", "REPLACE_WITH_YOUR_KEY");
        string host = "https://******/cognitiveservices/v1";


        //转换文本并保存
        public async Task textToSpeechAsync(string text, string savePath)
        {
            try
            {
                accessToken = await auth.FetchTokenAsync().ConfigureAwait(false);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex);
            }

            string body = "<speak version='1.0' xmlns='https://www.w3.org/2001/10/synthesis' xml:lang='"+locale+"'>"
              +"<voice name='"+voiceName+"'>" + text + "</voice></speak>";

            using (var client = new HttpClient())
            {
                using (var request = new HttpRequestMessage())
                {
                    // Set the HTTP method
                    request.Method = HttpMethod.Post;
                    // Construct the URI
                    request.RequestUri = new Uri(host);
                    // Set the content type header
                    request.Content = new StringContent(body, Encoding.UTF8, "application/ssml+xml");
                    // Set additional header, such as Authorization and User-Agent
                    request.Headers.Add("Authorization", "Bearer " + accessToken);
                    request.Headers.Add("Connection", "Keep-Alive");
                    // Update your resource name
                    request.Headers.Add("User-Agent", "YOUR_RESOURCE_NAME");
                    request.Headers.Add("X-Microsoft-OutputFormat", "riff-24khz-16bit-mono-pcm");
                    // Create a request
                    Console.WriteLine("Calling the TTS service. Please wait... \n");
                    using (var response = await client.SendAsync(request).ConfigureAwait(false))
                    {
                        response.EnsureSuccessStatusCode();
                        // Asynchronously read the response
                        using (var dataStream = await response.Content.ReadAsStreamAsync().ConfigureAwait(false))
                        {
                            Console.WriteLine("savePath:" + savePath);
                            using (var fileStream = new FileStream(savePath, FileMode.Create, FileAccess.Write, FileShare.Write))
                            {
                                await dataStream.CopyToAsync(fileStream).ConfigureAwait(false);
                                fileStream.Close();
                            }

                        }
                    }
                }
            }

        }
    }
}
