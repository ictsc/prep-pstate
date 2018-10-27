運用者向けガイド
======================================

デプロイメント
--------------------------------------


5.4で状態を確認した後に、以下のコマンドを実行します。

.. code-block:: bash

    KONG_API_IP=$(kubectl get all | grep kong-admin-ssl | awk '{print $3;}')
    # pstate本体のKong設定
    curl -k -i -X POST --url https://$KONG_API_IP:8444/services --data 'name=pstate-svc' --data 'url=http://pstate-service.default.svc.cluster.local'
    curl -k -i -X POST --url https://$KONG_API_IP:8444/apis -d 'name=pstate' -d 'upstream_url=http://pstate-service.default.svc.cluster.local/pstate' -d 'hosts=prep-dev.icttoracon.net' -d 'uris=/pstate'
    # pstateドキュメントのKong設定
    curl -k -i -X POST --url https://$KONG_API_IP:8444/services --data 'name=pstate-doc-svc' --data 'url=http://pstate-documentation-service.default.svc.cluster.local'
    curl -k -i -X POST --url https://$KONG_API_IP:8444/apis -d 'name=pstate-doc' -d 'upstream_url=http://pstate-documentation-service.default.svc.cluster.local/pstate-documentation/' -d 'hosts=prep-dev.icttoracon.net' -d 'uris=/pstate-documentation/'
    # pstateの静的ファイルのKong設定
    curl -k -i -X POST --url https://$KONG_API_IP:8444/services --data 'name=pstate-static-svc' --data 'url=http://pstate-staticfile-service.default.svc.cluster.local'
    curl -k -i -X POST --url https://$KONG_API_IP:8444/apis -d 'name=pstate-static' -d 'upstream_url=http://pstate-staticfile-service.default.svc.cluster.local/pstate-static/' -d 'hosts=prep-dev.icttoracon.net' -d 'uris=/pstate-static/'
