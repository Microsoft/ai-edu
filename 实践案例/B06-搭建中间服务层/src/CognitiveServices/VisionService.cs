// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for full license information.

using Newtonsoft.Json;
using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;

namespace CognitiveMiddlewareService.CognitiveServices
{
    public class VisionService : IVisionService
    {

        const string LandmarkEndpoint = "https://******/vision/v2.0/models/landmarks/analyze";
        const string CelebrityEndpoint = "https://******/vision/v2.0/models/celebrities/analyze";
        const string Key1 = "********************************";
        const string Key2 = "********************************";

        private readonly IHttpClientFactory httpClientFactory;

        public VisionService(IHttpClientFactory cf)
        {
            this.httpClientFactory = cf;
        }

        public async Task<Landmark> RecognizeLandmarkAsync(Stream imgStream)
        {
            VisionResult result = await this.MakePostRequest(LandmarkEndpoint, imgStream);
            if (result?.result?.landmarks?.Length > 0)
            {
                return result?.result?.landmarks[0];
            }
            return null;
        }

        public async Task<Celebrity> RecognizeCelebrityAsync(Stream imgStream)
        {
            VisionResult result = await this.MakePostRequest(CelebrityEndpoint, imgStream);
            if (result?.result?.celebrities?.Length > 0)
            {
                return result?.result?.celebrities[0];
            }
            return null;
        }

        private async Task<VisionResult> MakePostRequest(string uri, Stream imageStream)
        {
            try
            {
                using (HttpClient httpClient = httpClientFactory.CreateClient())
                {
                    using (StreamContent streamContent = new StreamContent(imageStream))
                    {
                        streamContent.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");
                        using (var request = new HttpRequestMessage(HttpMethod.Post, uri))
                        {
                            request.Content = streamContent;
                            request.Headers.Add("Ocp-Apim-Subscription-Key", Key1);
                            using (HttpResponseMessage response = await httpClient.SendAsync(request))
                            {
                                if (response.IsSuccessStatusCode)
                                {
                                    string resultString = await response.Content.ReadAsStringAsync();
                                    VisionResult result = JsonConvert.DeserializeObject<VisionResult>(resultString);
                                    return result;
                                }
                                else
                                {
                                }
                            }
                        }
                        return null;
                    }
                }
            }
            catch (Exception ex)
            {
                return null;
            }
        }
    }
}
