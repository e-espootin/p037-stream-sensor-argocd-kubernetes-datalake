#
kubectl create secret generic aws-s3-secret-etlop --from-literal=aws_access_key_id=AKIAYZDQEBCSC7K3QFYJ --from-literal=aws_secret_access_key=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
kubectl get secret
kubectl describe secret aws-s3-secret-etlop

# reference the secret in a pod
env: # Pass secret values as environment variables
    - name: AWS_ACCESS_KEY_ID
        valueFrom:
        secretKeyRef:
            name: aws-s3-secret-etlop
            key: AWS_ACCESS_KEY_ID
    - name: AWS_SECRET_ACCESS_KEY
        valueFrom:
        secretKeyRef:
            name: aws-s3-secret-etlop
            key: AWS_SECRET_ACCESS_KEY

kubectl apply -f pod-with-secret.yaml


# access secrets in python code

# inspect
kubectl exec -it example-pod -- env