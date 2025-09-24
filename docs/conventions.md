## Coding Conventions
1. Django models mutations are encapsulated as per [this convention](https://github.com/octoenergy/public-conventions/blob/main/conventions/django.md#encapsulate-model-mutation)
2. For any new graphql endpoint implemented, the preferred folder structure is
   * `core/graphql/endpoint_name` as `base_directory`
   * `base_directory/mutations.py` where all mutations endpoints live
   * `base_directory/queries.py` where all queries endpoints live
   * `base_directory/types.py` where the shared object type between mutations and queries live
   * `base_directory/feedback.py` where all the related endpoint feedback live

As much as possible all feedback is written per [this convention](https://github.com/octoenergy/public-conventions/blob/main/conventions/django.md#flash-messages)
  
* See `core/graphql/user` for an example of this convention

3. For any models created, we obfuscate the incremental ids so that we don't send them to the frontend
   * We thus use a custom `CustomDjangoObjectType` class in `core/graphql/public_identifier` for any graphql type
   * New models should inherit the `AuditIdentifierMixin` from `core/models/abstract` that automatically adds a uuid4 `public_id` field that is unique to each instance upon creation
   * See `core/graphql/user` for an example of such implementation
4. For any new migrations use the `--name` flag to provide a descriptive name