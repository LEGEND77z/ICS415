Shader "Introduction/myFirstShader"
{
    Properties
    {
        _MainTex ("text2D", 2D) = "white" {}
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fog

            #include "UnityCG.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                UNITY_FOG_COORDS(1)
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;

            v2f vert (appdata v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.uv, _MainTex);
                UNITY_TRANSFER_FOG(o, o.vertex);
                return o;
            }

            float opSmoothUnion(float d1, float d2, float k)
            {
                float h = clamp(0.5 + 0.5 * (d2 - d1) / k, 0.0, 1.0);
                return lerp(d2, d1, h) - k * h * (1.0 - h);
            }

            float sdSphere(float3 p, float s)
            {
                return length(p) - s;
            }

            float map(float3 p)
            {
                float d = 2.0;
                for (int i = 0; i < 16; i++) {
                    float fi = float(i);
                    float time = _Time.y * (frac(fi * 412.531 + 0.513) - 0.5) * 2.0;
                    d = opSmoothUnion(
                        sdSphere(p + sin(time + fi * float3(52.5126, 64.62744, 632.25)) * float3(2.0, 2.0, 0.8), lerp(0.5, 1.0, frac(fi * 412.531 + 0.5124))),
                        d,
                        0.4
                    );
                }
                return d;
            }

            float3 calcNormal(in float3 p)
            {
                const float h = 1e-5;
                const float2 k = float2(1, -1);
                return normalize( k.xyy * map(p + k.xyy * h) +
                                  k.yyx * map(p + k.yyx * h) +
                                  k.yxy * map(p + k.yxy * h) +
                                  k.xxx * map(p + k.xxx * h) );
            }

            fixed4 frag(v2f i) : SV_Target
            {
                float2 uv = i.uv;

                // Use _ScreenParams to obtain the correct aspect ratio.
                float aspect = _ScreenParams.x / _ScreenParams.y;
                float3 rayOri = float3((uv - 0.5) * float2(aspect, 1.0) * 6.0, 3.0);
                float3 rayDir = float3(0.0, 0.0, -1.0);

                float depth = 0.0;
                float3 p;

                for (int j = 0; j < 64; j++) {
                    p = rayOri + rayDir * depth;
                    float dist = map(p);
                    depth += dist;
                    if (dist < 1e-6) {
                        break;
                    }
                }

                depth = min(6.0, depth);
                float3 n = calcNormal(p);
                float b = max(0.0, dot(n, float3(0.577, 0.577, 0.577)));
                float3 color = (0.5 + 0.5 * cos((b + _Time.y * 3.0) + uv.xyx * 2.0 + float3(0,2,4))) * (0.85 + b * 0.35);
                color *= exp(-depth * 0.15);

                fixed4 col = tex2D(_MainTex, i.uv);
                col.rgb = color;
                col.a = 1.0 - (depth - 0.5) / 2.0;

                UNITY_APPLY_FOG(i.fogCoord, col);

                return col;
            }
            ENDCG
        }
    }
}
