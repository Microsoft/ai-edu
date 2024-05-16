// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for full license information.

using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using System.Web;

namespace CartoonTranslate
{
    class CognitiveServiceAgent
    {
        const string OcrEndPointV1 = "https://******/vision/v2.0/ocr?detectOrientation=true&language=";
        const string OcrEndPointV2 = "https://******/vision/v2.0/recognizeText?mode=Printed";
        const string VisionKey1 = "********************************";
        const string VisionKey2 = "********************************";
        const string UrlContentTemplate = "{{\"url\":\"{0}\"}}";

        const string TranslateEndPoint = "https://******/translate?api-version=3.0&from={0}&to={1}";
        const string TKey1 = "********************************";
        const string TKey2 = "********************************";

        public static async Task<List<string>> DoTranslate(List<string> text, string fromLanguage, string toLanguage)
        {
            try
            {
                using (HttpClient hc = new HttpClient())
                {
                    hc.DefaultRequestHeaders.Add("Ocp-Apim-Subscription-Key", TKey1);
                    string jsonBody = CreateJsonBodyElement(text);
                    StringContent content = new StringContent(jsonBody, Encoding.UTF8, "application/json");
                    string uri = string.Format(TranslateEndPoint, fromLanguage, toLanguage);
                    HttpResponseMessage resp = await hc.PostAsync(uri, content);
                    string json = await resp.Content.ReadAsStringAsync();
                    var ro = Newtonsoft.Json.JsonConvert.DeserializeObject<List<TranslateResult.Class1>>(json);
                    List<string> list = new List<string>();
                    foreach(TranslateResult.Class1 c in ro)
                    {
                        list.Add(c.translations[0].text);
                    }
                    return list;
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine(ex.Message);
                return null;
            }
        }

        private static string CreateJsonBodyElement(List<string> text)
        {
            var a = text.Select(t => new { Text = t }).ToList();
            var b = JsonConvert.SerializeObject(a);
            return b;
        }


        public static async Task<NewOcrResult.Rootobject> DoRecognizeText(string imageUrl)
        {
            try
            {
                using (HttpClient hc = new HttpClient())
                {
                    ByteArrayContent content = CreateHeader(hc, imageUrl);
                    HttpResponseMessage resp = await hc.PostAsync(OcrEndPointV2, content);
                    string json = string.Empty;
                    if (resp.StatusCode == System.Net.HttpStatusCode.Accepted)
                    {
                        var headers = resp.Headers;
                        foreach (var kv in headers)
                        {
                            if (kv.Key == "Operation-Location")
                            {
                                string url = kv.Value.First();
                                while (true)
                                {
                                    // check status every 200ms
                                    await Task.Delay(200);
                                    json = await CheckStatus(url);
                                    if (!string.IsNullOrEmpty(json))
                                    {
                                        break;
                                    }
                                }
                                break;
                            }
                        }
                    }
                    if (string.IsNullOrEmpty(json))
                    {
                        return null;
                    }
                    else
                    {
                        NewOcrResult.Rootobject ro = Newtonsoft.Json.JsonConvert.DeserializeObject<NewOcrResult.Rootobject>(json);
                        return ro;
                    }
                }
            }
            catch (Exception ex)
            {
                Debug.Write(ex.Message);
                return null;
            }
        }

        private static async Task<string> CheckStatus(string url)
        {
            using (HttpClient hc = new HttpClient())
            {
                hc.DefaultRequestHeaders.Add("Ocp-Apim-Subscription-Key", VisionKey1);
                HttpResponseMessage resp = await hc.GetAsync(url);
                if (resp.StatusCode == System.Net.HttpStatusCode.OK)
                {
                    string result = await resp.Content.ReadAsStringAsync();
                    if (result.Contains("Running"))
                    {
                        return null;
                    }
                    return result;
                }
                else
                {
                    return null;
                }
            }
        }


        /// <summary>
        /// 
        /// </summary>
        /// <param name="imageUrl"></param>
        /// <param name="language">en, ja, zh</param>
        /// <returns></returns>
        public static async Task<OcrResult.Rootobject> DoOCR(string imageUrl, string language)
        {
            try
            {
                using (HttpClient hc = new HttpClient())
                {
                    ByteArrayContent content = CreateHeader(hc, imageUrl);
                    var uri = OcrEndPointV1 + language;
                    HttpResponseMessage resp = await hc.PostAsync(uri, content);
                    string result = string.Empty;
                    if (resp.StatusCode == System.Net.HttpStatusCode.OK)
                    {
                        string json = await resp.Content.ReadAsStringAsync();
                        Debug.WriteLine(json);
                        OcrResult.Rootobject ro = Newtonsoft.Json.JsonConvert.DeserializeObject<OcrResult.Rootobject>(json);
                        return ro;
                    }
                }
                return null;
            }
            catch (Exception ex)
            {
                Debug.Write(ex.Message);
                return null;
            }
        }

        private static ByteArrayContent CreateHeader(HttpClient hc, string imageUrl)
        {
            hc.DefaultRequestHeaders.Add("Ocp-Apim-Subscription-Key", VisionKey1);
            string body = string.Format(UrlContentTemplate, imageUrl);
            byte[] byteData = Encoding.UTF8.GetBytes(body);
            var content = new ByteArrayContent(byteData);
            content.Headers.ContentType = new MediaTypeHeaderValue("application/json");
            return content;
        }

    }
}
